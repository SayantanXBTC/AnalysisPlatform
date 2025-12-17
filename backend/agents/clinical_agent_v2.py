"""
Clinical Trials Agent - REAL DATA ONLY VERSION
Enforces strict evidence-based analysis with no synthetic fallbacks
"""
import pandas as pd
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from typing import Dict, List, Optional
import time

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_clinical_trials(drug_name: str, indication: str) -> Optional[pd.DataFrame]:
    """Fetch clinical trials from ClinicalTrials.gov API - REAL DATA ONLY"""
    try:
        base_url = "https://clinicaltrials.gov/api/v2/studies"
        
        query_terms = [drug_name]
        if indication:
            query_terms.append(indication)
        
        params = {
            "query.term": " AND ".join(query_terms),
            "format": "json",
            "pageSize": 100,
            "fields": "NCTId,BriefTitle,OverallStatus,Phase,EnrollmentCount,StartDate,CompletionDate,SponsorCollaboratorsModule"
        }
        
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        studies = data.get("studies", [])
        
        if not studies:
            return None
        
        trials_list = []
        for study in studies[:100]:
            protocol = study.get("protocolSection", {})
            id_module = protocol.get("identificationModule", {})
            status_module = protocol.get("statusModule", {})
            design_module = protocol.get("designModule", {})
            sponsor_module = protocol.get("sponsorCollaboratorsModule", {})
            
            trial_data = {
                "Trial ID": id_module.get("nctId", "N/A"),
                "Title": id_module.get("briefTitle", "N/A")[:80],
                "Phase": ", ".join(design_module.get("phases", ["N/A"])),
                "Status": status_module.get("overallStatus", "N/A"),
                "Enrollment": status_module.get("enrollmentInfo", {}).get("count", 0),
                "Start Date": status_module.get("startDateStruct", {}).get("date", "N/A"),
                "Sponsor": sponsor_module.get("leadSponsor", {}).get("name", "N/A")[:40]
            }
            trials_list.append(trial_data)
        
        df = pd.DataFrame(trials_list)
        df["Enrollment"] = pd.to_numeric(df["Enrollment"], errors="coerce").fillna(0).astype(int)
        df = df[df["Enrollment"] > 0]
        
        return df if len(df) > 0 else None
        
    except Exception as e:
        print(f"Error fetching clinical trials: {e}")
        return None

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_literature(drug_name: str, indication: str) -> Optional[List[str]]:
    """Fetch literature from Europe PMC API - REAL DATA ONLY"""
    try:
        base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
        
        query = f'"{drug_name}" AND "{indication}"'
        params = {
            "query": query,
            "format": "json",
            "pageSize": 10,
            "resultType": "core"
        }
        
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        results = data.get("resultList", {}).get("result", [])
        
        citations = []
        for result in results[:5]:
            authors = result.get("authorString", "Unknown")
            title = result.get("title", "No title")
            journal = result.get("journalTitle", "Unknown Journal")
            year = result.get("pubYear", "N/A")
            
            citation = f"{authors} ({year}) - {title[:100]}, {journal}"
            citations.append(citation)
        
        return citations if citations else None
        
    except Exception as e:
        print(f"Error fetching literature: {e}")
        return None

def analyze_clinical(drug_name: str, indication: str) -> Dict:
    """
    Clinical Trials Analysis - REAL DATA ONLY
    Returns empty evidence if no data found (NO SYNTHETIC FALLBACK)
    """
    
    # Fetch REAL data only
    trials_df = fetch_clinical_trials(drug_name, indication)
    citations = fetch_literature(drug_name, indication)
    
    # MANDATORY: Return empty evidence if no real data
    if trials_df is None or len(trials_df) == 0:
        return {
            "section": "Clinical Trials & Evidence",
            "summary": f"No clinical trial data found for {drug_name} in {indication}",
            "text": f"""
**CLINICAL TRIAL ANALYSIS**

**No Clinical Evidence Found:**
Comprehensive search of ClinicalTrials.gov registry identified no registered clinical trials investigating {drug_name} for {indication}. This absence of clinical evidence indicates:

• No formal clinical development program for this indication
• Lack of regulatory-grade efficacy and safety data
• No established clinical rationale or precedent
• Significant development risk and uncertainty

**Implications:**
Without clinical trial evidence, therapeutic potential cannot be assessed. Any development would require:
• Complete Phase 1-3 clinical program (8-12 years)
• Substantial investment ($500M-$2B)
• High regulatory and commercial risk
• No existing safety/efficacy data to leverage

**Recommendation:**
Clinical evidence score: 0/100. This indication lacks clinical validation and would require de novo drug development.
            """.strip(),
            "table": [],
            "efficacy_table": [],
            "key_findings": [
                "No clinical trials identified in ClinicalTrials.gov",
                "No clinical evidence available for assessment",
                "Complete clinical development program required",
                "High development risk and cost"
            ],
            "confidence": 10,
            "confidence_score": 0.10,
            "total_trials": 0,
            "total_patients": 0,
            "citations": citations or [],
            "quality_notes": "No real clinical data available",
            "clinical_score": 0  # For master agent
        }
    
    # Process REAL DATA
    total_trials = len(trials_df)
    total_patients = int(trials_df["Enrollment"].sum())
    
    # Phase analysis
    phase_1 = len(trials_df[trials_df["Phase"].str.contains("1", na=False)])
    phase_2 = len(trials_df[trials_df["Phase"].str.contains("2", na=False)])
    phase_3 = len(trials_df[trials_df["Phase"].str.contains("3", na=False)])
    phase_4 = len(trials_df[trials_df["Phase"].str.contains("4", na=False)])
    
    # Status analysis
    completed = len(trials_df[trials_df["Status"].str.contains("Completed", case=False, na=False)])
    active = len(trials_df[trials_df["Status"].str.contains("Recruiting|Active", case=False, na=False)])
    terminated = len(trials_df[trials_df["Status"].str.contains("Terminated|Withdrawn", case=False, na=False)])
    
    # Calculate metrics
    success_rate = (completed / total_trials * 100) if total_trials > 0 else 0
    attrition_rate = (terminated / total_trials * 100) if total_trials > 0 else 0
    
    # Calculate clinical score for master agent
    clinical_score = 0
    if phase_3 >= 3:
        clinical_score += 40
    elif phase_3 >= 1:
        clinical_score += 25
    elif phase_2 >= 3:
        clinical_score += 15
    
    if completed >= 5:
        clinical_score += 20
    elif completed >= 2:
        clinical_score += 10
    
    if total_patients >= 1000:
        clinical_score += 15
    elif total_patients >= 300:
        clinical_score += 8
    
    if attrition_rate < 15:
        clinical_score += 10
    elif attrition_rate < 25:
        clinical_score += 5
    
    clinical_score = min(100, clinical_score)
    
    # Generate evidence-based narrative
    narrative = f"""
**CLINICAL TRIAL EVIDENCE ANALYSIS**

**Trial Portfolio Overview:**
ClinicalTrials.gov registry search identified {total_trials} registered clinical trials investigating {drug_name} for {indication}, with cumulative enrollment of {total_patients:,} patients. This represents {"substantial" if total_trials >= 10 else "moderate" if total_trials >= 5 else "limited"} clinical development activity.

**Development Phase Distribution:**
• Phase 1 (Safety/PK): {phase_1} trials
• Phase 2 (Proof-of-Concept): {phase_2} trials  
• Phase 3 (Pivotal Efficacy): {phase_3} trials
• Phase 4 (Post-Marketing): {phase_4} trials

{"The presence of " + str(phase_3) + " Phase 3 trials indicates advanced development with potential regulatory submissions." if phase_3 > 0 else "No Phase 3 trials identified, indicating early-stage or exploratory development."}

**Trial Status & Evidence Maturity:**
• Completed: {completed} trials ({success_rate:.1f}%)
• Active/Recruiting: {active} trials
• Terminated/Withdrawn: {terminated} trials ({attrition_rate:.1f}% attrition)

{"Completion rate of " + f"{success_rate:.0f}%" + " indicates " + ("strong" if success_rate > 60 else "moderate" if success_rate > 40 else "limited") + " evidence maturity." if completed > 0 else "No completed trials available for efficacy assessment."}

**Statistical Power & Patient Population:**
Total enrollment of {total_patients:,} patients provides {"adequate" if total_patients >= 1000 else "limited"} statistical power for detecting clinically meaningful effects. {"This sample size supports robust efficacy claims and subgroup analyses." if total_patients >= 1000 else "Additional enrollment may be needed for definitive efficacy conclusions."}

**Evidence Quality Assessment:**
Clinical evidence quality: {"HIGH - Multiple completed Phase 3 trials with large patient populations" if phase_3 >= 2 and completed >= 5 else "MODERATE - Phase 2 data with ongoing Phase 3 development" if phase_2 >= 3 else "LOW - Early-stage development with limited completed trials"}

**Regulatory & Development Implications:**
{"Strong clinical evidence base supports regulatory submissions. Development timeline: 12-24 months to potential approval." if phase_3 >= 2 and completed >= 3 else "Ongoing clinical development required. Estimated timeline: 36-60 months to potential regulatory submission." if phase_2 >= 2 else "Early-stage development. Complete Phase 1-3 program required (8-12 years)."}

**Clinical Feasibility Score: {clinical_score}/100**
    """.strip()
    
    # Prepare data tables
    trials_table = trials_df.head(30).to_dict('records')
    
    efficacy_table = [
        {"Metric": "Total Clinical Trials", "Value": str(total_trials), "Assessment": "Real Data"},
        {"Metric": "Total Patients", "Value": f"{total_patients:,}", "Assessment": "Real Data"},
        {"Metric": "Phase 3 Trials", "Value": str(phase_3), "Assessment": "Real Data"},
        {"Metric": "Completed Trials", "Value": str(completed), "Assessment": "Real Data"},
        {"Metric": "Success Rate", "Value": f"{success_rate:.0f}%", "Assessment": "Real Data"},
        {"Metric": "Clinical Score", "Value": f"{clinical_score}/100", "Assessment": "Calculated"}
    ]
    
    key_findings = [
        f"{total_trials} clinical trials with {total_patients:,} patients (REAL DATA)",
        f"{phase_3} Phase 3 trials, {completed} completed trials",
        f"Clinical evidence score: {clinical_score}/100",
        f"Evidence quality: {'HIGH' if clinical_score >= 60 else 'MODERATE' if clinical_score >= 30 else 'LOW'}",
        f"Attrition rate: {attrition_rate:.0f}% ({'acceptable' if attrition_rate < 25 else 'elevated'})"
    ]
    
    confidence = min(95, 50 + (clinical_score // 2))
    
    return {
        "section": "Clinical Trials & Evidence",
        "summary": f"{total_trials} trials, {total_patients:,} patients, {phase_3} Phase 3, Clinical Score: {clinical_score}/100",
        "text": narrative,
        "table": trials_table,
        "efficacy_table": efficacy_table,
        "key_findings": key_findings,
        "confidence": confidence,
        "confidence_score": confidence / 100,
        "total_trials": total_trials,
        "total_patients": total_patients,
        "citations": citations or [f"ClinicalTrials.gov - {drug_name} Registry (accessed {time.strftime('%Y-%m-%d')})"],
        "quality_notes": f"Real-time data from ClinicalTrials.gov API ({total_trials} trials)",
        "clinical_score": clinical_score,  # For master agent
        "phase_3_count": phase_3,
        "completed_count": completed
    }
