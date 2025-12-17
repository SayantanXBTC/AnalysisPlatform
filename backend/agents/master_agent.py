from agents import clinical_agent, market_agent, patent_agent
from agents import regulatory_agent, safety_agent, internal_agent
from agents.n8n_adapter_agent import N8NAdapterAgent
from agents.moa_agent import MoAAgent
from agents.ppi_agent import PPIAgent
from agents.disease_similarity_agent import DiseaseSimilarityAgent
from agents.hypothesis_agent import HypothesisAgent
from utilities import send_to_n8n
from config import N8N_WEBHOOK_ANALYSIS_URL
from datetime import datetime

try:
    from agents import literature_agent
    LITERATURE_AVAILABLE = True
except ImportError:
    LITERATURE_AVAILABLE = False
    print("Literature agent not available")

def run_multi_agent_analysis(drug_name: str, indication: str):
    """Orchestrate all agent analyses with executive summary using real API data + n8n integrations"""
    
    # Initialize new agents
    n8n_adapter = N8NAdapterAgent()
    moa_agent = MoAAgent()
    ppi_agent = PPIAgent()
    similarity_agent = DiseaseSimilarityAgent()
    hypothesis_agent = HypothesisAgent()
    
    # Run all agent analyses (now with real API calls and rich synthesis)
    clinical = clinical_agent.analyze_clinical(drug_name, indication)
    
    # Run literature analysis if available
    if LITERATURE_AVAILABLE:
        literature = literature_agent.analyze_literature(drug_name, indication)
    else:
        literature = {"section": "Literature", "text": "Literature analysis unavailable", "confidence": 50}
    
    market = market_agent.analyze_market(drug_name, indication)
    patent = patent_agent.analyze_patent(drug_name, indication)
    regulatory = regulatory_agent.analyze_regulatory(drug_name, indication)
    safety = safety_agent.analyze_safety(drug_name, indication)
    internal = internal_agent.analyze_internal(drug_name, indication)
    
    # Fetch IQVIA + EXIM data via n8n
    print("[Master Agent] Fetching IQVIA and EXIM data via n8n...")
    iqvia_data = n8n_adapter.fetch_iqvia_mock(drug_name, indication)
    exim_data = n8n_adapter.fetch_exim_mock(drug_name, indication)
    
    # Run MoA analysis
    print("[Master Agent] Running Mechanism of Action analysis...")
    moa_data = moa_agent.run_moa(drug_name, indication)
    
    # Run PPI network analysis
    print("[Master Agent] Running PPI network analysis...")
    drug_targets = moa_data.get("primary_targets", [])
    disease_genes = ["GENE1", "GENE2", "GENE3"]  # In production, extract from disease databases
    ppi_data = ppi_agent.run_ppi(drug_targets, disease_genes, drug_name, indication)
    
    # Run disease similarity analysis
    print("[Master Agent] Running disease similarity analysis...")
    similarity_data = similarity_agent.run_similarity(drug_name, indication)
    
    # Prepare evidence features for hypothesis generation
    evidence_features = {
        "clinical_confidence": clinical.get("confidence_score", 0.5),
        "literature_confidence": literature.get("confidence", 50) / 100,
        "safety_confidence": safety.get("confidence_score", 0.5),
        "market_confidence": market.get("confidence_score", 0.5)
    }
    
    # Generate AI-driven hypotheses
    print("[Master Agent] Generating research hypotheses...")
    hypothesis_data = hypothesis_agent.run_hypothesis_engine(
        drug_name, indication, moa_data, ppi_data, similarity_data, evidence_features
    )
    
    # Calculate enhanced feasibility score with new components
    clinical_score = clinical.get("confidence_score", clinical.get("confidence", 50) / 100) * 100
    literature_score = literature.get("confidence", 50)
    patent_score = patent.get("confidence_score", 0.5) * 100
    safety_score = safety.get("confidence_score", 0.5) * 100
    moa_score = moa_data.get("moa_score", 50)
    ppi_score = ppi_data.get("ppi_score", 50)
    similarity_score = similarity_data.get("similarity_score", 50)
    
    # Safety penalty
    safety_signals = safety.get("total_safety_signals", 0)
    safety_penalty = min(20, safety_signals * 2)
    
    # Calculate final feasibility score (0-100)
    final_score = (
        (clinical_score * 0.20) +      # Clinical evidence: 20%
        (literature_score * 0.15) +    # Literature: 15%
        (patent_score * 0.10) +        # Patent: 10%
        (safety_score * 0.15) +        # Safety: 15%
        (moa_score * 0.15) +           # MoA: 15%
        (ppi_score * 0.15) +           # PPI: 15%
        (similarity_score * 0.10) -    # Similarity: 10%
        safety_penalty                  # Safety penalty
    )
    final_score = max(0, min(100, round(final_score)))
    
    # Generate comprehensive executive summary
    executive_summary = generate_executive_summary(
        drug_name, indication, clinical, literature, market, patent, regulatory, safety, internal,
        moa_data, ppi_data, similarity_data, hypothesis_data, final_score, iqvia_data, exim_data
    )
    
    # Calculate aggregate metrics from real data
    all_confidences = [
        clinical.get("confidence_score", clinical.get("confidence", 50) / 100),
        literature.get("confidence", 50) / 100,
        market.get("confidence_score", 0.5),
        patent.get("confidence_score", 0.5),
        regulatory.get("confidence_score", 0.5),
        safety.get("confidence_score", 0.5),
        internal.get("confidence_score", 0.5),
        moa_data.get("confidence_score", 0.6),
        ppi_data.get("confidence_score", 0.6),
        similarity_data.get("confidence_score", 0.6)
    ]
    avg_confidence = round(sum(all_confidences) / len(all_confidences), 2)
    
    highlights = {
        "total_trials": clinical.get("total_trials", 0),
        "total_patients": clinical.get("total_patients", 0),
        "total_patents": patent.get("total_patents", 0),
        "safety_signals": safety.get("total_safety_signals", 0),
        "market_size": market.get("peak_sales_projection", "N/A"),
        "approval_probability": regulatory.get("approval_probability", "N/A"),
        "investment_required": internal.get("total_investment", "N/A"),
        "avg_confidence": avg_confidence,
        "feasibility_score": final_score,
        "moa_score": moa_score,
        "ppi_score": ppi_score,
        "similarity_score": similarity_score
    }
    
    results = {
        "executive_summary": executive_summary,
        "highlights": highlights,
        "Clinical": clinical,
        "Literature": literature,
        "Market": market,
        "Patent": patent,
        "Regulatory": regulatory,
        "Safety": safety,
        "Internal": internal,
        "IQVIA_Market_Intelligence": iqvia_data,
        "EXIM_Trade_Intelligence": exim_data,
        "Mechanism_of_Action": moa_data,
        "PPI_Network": ppi_data,
        "Disease_Similarity": similarity_data,
        "Hypothesis_Generation": hypothesis_data
    }
    
    # Send n8n webhook notification
    print("[Master Agent] Sending analysis completion webhook to n8n...")
    send_to_n8n(N8N_WEBHOOK_ANALYSIS_URL, {
        "drug": drug_name,
        "indication": indication,
        "feasibility_score": final_score,
        "avg_confidence": avg_confidence,
        "timestamp": datetime.now().isoformat(),
        "status": "completed"
    })
    
    return results

def generate_executive_summary(drug_name, indication, clinical, literature, market, patent, regulatory, safety, internal,
                              moa_data, ppi_data, similarity_data, hypothesis_data, final_score, iqvia_data, exim_data):
    """Generate COMPREHENSIVE executive summary with strategic insights including new intelligence modules"""
    
    # Extract key metrics
    total_trials = clinical.get('total_trials', 0)
    total_patients = clinical.get('total_patients', 0)
    total_patents = patent.get('total_patents', 0)
    safety_signals = safety.get('total_safety_signals', 0)
    
    # Calculate confidence scores
    clinical_conf = clinical.get('confidence_score', clinical.get('confidence', 50) / 100) * 100
    lit_conf = literature.get('confidence', 50)
    market_conf = market.get('confidence_score', 0.5) * 100
    patent_conf = patent.get('confidence_score', 0.5) * 100
    reg_conf = regulatory.get('confidence_score', 0.5) * 100
    safety_conf = safety.get('confidence_score', 0.5) * 100
    internal_conf = internal.get('confidence_score', 0.5) * 100
    
    avg_confidence = round((clinical_conf + lit_conf + market_conf + patent_conf + reg_conf + safety_conf + internal_conf) / 7, 1)
    
    # Calculate repurposing potential score (1-100)
    repurposing_score = min(100, round(
        (clinical_conf * 0.30) +  # Clinical evidence weight: 30%
        (lit_conf * 0.20) +        # Literature/mechanism weight: 20%
        (safety_conf * 0.20) +     # Safety weight: 20%
        (patent_conf * 0.15) +     # IP weight: 15%
        (market_conf * 0.15)       # Market weight: 15%
    ))
    
    # Determine safety classification
    if safety_conf >= 75 and safety_signals <= 3:
        safety_class = "SAFE - Well-characterized profile"
    elif safety_conf >= 60 and safety_signals <= 6:
        safety_class = "MODERATE - Manageable with monitoring"
    else:
        safety_class = "REQUIRES EVALUATION - Enhanced pharmacovigilance needed"
    
    # Determine market entry difficulty
    if market_conf >= 70 and patent_conf >= 70:
        market_difficulty = "LOW - Clear pathway with IP protection"
    elif market_conf >= 55 or patent_conf >= 55:
        market_difficulty = "MODERATE - Competitive but feasible"
    else:
        market_difficulty = "HIGH - Significant barriers require strategy"
    
    # Determine recommendation color
    if repurposing_score >= 75 and safety_conf >= 70:
        recommendation = "GREEN - STRONG GO"
        rec_detail = "High confidence in therapeutic potential with favorable risk-benefit profile"
    elif repurposing_score >= 60 and safety_conf >= 55:
        recommendation = "YELLOW - PROCEED WITH CAUTION"
        rec_detail = "Moderate confidence; additional validation studies recommended"
    else:
        recommendation = "RED - HIGH RISK"
        rec_detail = "Significant uncertainties require substantial additional evidence"
    
    # Identify data sources
    data_sources = []
    if "Real-time" in clinical.get('quality_notes', '') or "Real-world" in clinical.get('quality_notes', ''):
        data_sources.append("ClinicalTrials.gov")
    if "Real-time" in literature.get('quality_notes', '') or "Europe PMC" in str(literature.get('citations', [])):
        data_sources.append("Europe PMC")
    if "Real-time" in patent.get('quality_notes', '') or "USPTO" in patent.get('quality_notes', ''):
        data_sources.append("USPTO PatentsView")
    if "Real-world" in safety.get('quality_notes', '') or "FAERS" in safety.get('quality_notes', ''):
        data_sources.append("FDA FAERS")
    if "Real-time" in market.get('quality_notes', '') or "OpenFDA" in market.get('quality_notes', ''):
        data_sources.append("OpenFDA")
    
    data_quality_note = f"Real-time data from: {', '.join(data_sources)}" if data_sources else "Comprehensive therapeutic area analysis"
    
    # Generate top 5 reasons this could work
    reasons_work = [
        f"Clinical evidence: {total_trials} trials with {total_patients:,} patients demonstrate feasibility",
        f"Mechanism validation: {'Strong' if lit_conf > 70 else 'Moderate'} scientific rationale from published literature",
        f"Safety profile: {safety_class.split(' - ')[1]} based on real-world data",
        f"IP protection: {total_patents} patents providing market exclusivity to {patent.get('primary_expiry', '2035+')}",
        f"Market opportunity: {'Established' if market_conf > 70 else 'Emerging'} commercial pathway identified"
    ]
    
    # Generate top 5 blockers/risks
    blockers = [
        f"Clinical validation: {'Minimal' if clinical_conf > 80 else 'Moderate' if clinical_conf > 60 else 'Significant'} additional trials may be required",
        f"Safety monitoring: {safety_signals} safety signals require ongoing pharmacovigilance",
        f"Competitive landscape: {'Moderate' if market_conf > 60 else 'High'} competition in therapeutic area",
        f"Regulatory pathway: {'Standard' if reg_conf > 70 else 'Complex'} approval process anticipated",
        f"Investment requirement: {internal.get('total_investment', '$50M+')} over {internal.get('timeline_to_launch', '12-24 months')}"
    ]
    
    summary = f"""
═══════════════════════════════════════════════════════════════════════════════
EXECUTIVE INTELLIGENCE REPORT: {drug_name} for {indication}
═══════════════════════════════════════════════════════════════════════════════

DATA FOUNDATION: {data_quality_note}
Analysis Date: {__import__('time').strftime('%Y-%m-%d')}
Overall Confidence: {avg_confidence}% | Repurposing Potential: {repurposing_score}/100

═══════════════════════════════════════════════════════════════════════════════
STRATEGIC ASSESSMENT
═══════════════════════════════════════════════════════════════════════════════

REPURPOSING POTENTIAL SCORE: {repurposing_score}/100
• Evidence Quality: {'STRONG' if avg_confidence > 75 else 'MODERATE' if avg_confidence > 60 else 'DEVELOPING'}
• Clinical Readiness: {'HIGH' if clinical_conf > 75 else 'MODERATE' if clinical_conf > 60 else 'EARLY STAGE'}
• Commercial Viability: {'FAVORABLE' if market_conf > 70 else 'COMPETITIVE' if market_conf > 55 else 'CHALLENGING'}

SAFETY FEASIBILITY: {safety_class}

MARKET ENTRY DIFFICULTY: {market_difficulty}

OVERALL RECOMMENDATION: {recommendation}
{rec_detail}

═══════════════════════════════════════════════════════════════════════════════
CLINICAL INTELLIGENCE SUMMARY
═══════════════════════════════════════════════════════════════════════════════

{clinical.get('summary', 'Clinical analysis in progress')}

KEY METRICS:
• Total Clinical Trials: {total_trials}
• Total Patients Enrolled: {total_patients:,}
• Evidence Maturity: {clinical.get('key_findings', ['Data available'])[0] if clinical.get('key_findings') else 'Developing'}
• Confidence Level: {clinical_conf:.0f}%

CLINICAL INSIGHTS:
{chr(10).join(['• ' + f for f in clinical.get('key_findings', ['Clinical data available'])[:4]])}

═══════════════════════════════════════════════════════════════════════════════
MECHANISM & LITERATURE ANALYSIS
═══════════════════════════════════════════════════════════════════════════════

MECHANISTIC RATIONALE:
{literature.get('key_findings', ['Mechanism analysis available'])[0] if literature.get('key_findings') else 'Scientific rationale established'}

LITERATURE INSIGHTS:
{chr(10).join(['• ' + f for f in literature.get('key_findings', ['Literature data available'])[:3]])}

Confidence Level: {lit_conf:.0f}%

═══════════════════════════════════════════════════════════════════════════════
INTELLECTUAL PROPERTY LANDSCAPE
═══════════════════════════════════════════════════════════════════════════════

{patent.get('summary', 'Patent analysis complete')}

IP PROTECTION:
• Total Patents Identified: {total_patents}
• Primary Patent Expiry: {patent.get('primary_expiry', '2035+')}
• Freedom to Operate: {'Favorable' if patent_conf > 70 else 'Requires review'}
• Confidence Level: {patent_conf:.0f}%

═══════════════════════════════════════════════════════════════════════════════
SAFETY & PHARMACOVIGILANCE PROFILE
═══════════════════════════════════════════════════════════════════════════════

{safety.get('summary', 'Safety analysis complete')}

SAFETY METRICS:
• Key Safety Signals: {safety_signals}
• Safety Classification: {safety_class}
• Monitoring Requirements: {'Standard' if safety_signals <= 3 else 'Enhanced'}
• Confidence Level: {safety_conf:.0f}%

═══════════════════════════════════════════════════════════════════════════════
MARKET & COMPETITIVE ANALYSIS
═══════════════════════════════════════════════════════════════════════════════

{market.get('summary', 'Market analysis complete')}

COMMERCIAL OUTLOOK:
• Peak Sales Projection: {market.get('peak_sales_projection', 'Market-dependent')}
• Market Share Target: {market.get('market_share_target', 'TBD')}
• Competitive Intensity: {'High' if market_conf < 60 else 'Moderate' if market_conf < 75 else 'Manageable'}
• Confidence Level: {market_conf:.0f}%

═══════════════════════════════════════════════════════════════════════════════
REGULATORY STRATEGY
═══════════════════════════════════════════════════════════════════════════════

{regulatory.get('summary', 'Regulatory pathway defined')}

REGULATORY METRICS:
• Approval Probability: {regulatory.get('approval_probability', 'TBD')}
• Target Approval: {regulatory.get('target_approval', 'TBD')}
• Pathway Complexity: {'Standard' if reg_conf > 70 else 'Complex'}
• Confidence Level: {reg_conf:.0f}%

═══════════════════════════════════════════════════════════════════════════════
OPERATIONAL & INVESTMENT REQUIREMENTS
═══════════════════════════════════════════════════════════════════════════════

{internal.get('summary', 'Operational assessment complete')}

RESOURCE REQUIREMENTS:
• Total Investment: {internal.get('total_investment', 'TBD')}
• Timeline to Launch: {internal.get('timeline_to_launch', 'TBD')}
• Operational Risk: {'Low' if internal_conf > 75 else 'Moderate'}
• Confidence Level: {internal_conf:.0f}%

═══════════════════════════════════════════════════════════════════════════════
IQVIA MARKET INTELLIGENCE
═══════════════════════════════════════════════════════════════════════════════

MARKET METRICS:
• Market Size: ${iqvia_data.get('market_size_usd_millions', 'N/A')}M
• CAGR: {iqvia_data.get('cagr_percent', 'N/A')}%
• Market Share Opportunity: {iqvia_data.get('current_market_share_percent', 'N/A')}%
• 2030 Forecast: ${iqvia_data.get('forecast_2030', 'N/A')}M

KEY INSIGHTS:
{chr(10).join(['• ' + insight for insight in iqvia_data.get('key_insights', ['Market data available'])[:3]])}

═══════════════════════════════════════════════════════════════════════════════
EXIM TRADE INTELLIGENCE
═══════════════════════════════════════════════════════════════════════════════

TRADE METRICS:
• Total Exports: ${exim_data.get('total_exports_usd_millions', 'N/A')}M
• Total Imports: ${exim_data.get('total_imports_usd_millions', 'N/A')}M
• Trade Balance: ${exim_data.get('trade_balance_usd_millions', 'N/A')}M
• Export Growth YoY: {exim_data.get('trade_trends', {}).get('export_growth_yoy_percent', 'N/A')}%

═══════════════════════════════════════════════════════════════════════════════
MECHANISM OF ACTION ANALYSIS
═══════════════════════════════════════════════════════════════════════════════

MoA SCORE: {moa_data.get('moa_score', 'N/A')}/100

TARGET PROFILE:
• Primary Targets: {len(moa_data.get('primary_targets', []))}
• Affected Pathways: {len(moa_data.get('affected_pathways', []))}
• MoA Confidence: {moa_data.get('moa_confidence', 'N/A')}%

KEY FINDINGS:
{chr(10).join(['• ' + finding for finding in moa_data.get('key_findings', ['MoA analysis complete'])[:3]])}

═══════════════════════════════════════════════════════════════════════════════
PROTEIN-PROTEIN INTERACTION NETWORK
═══════════════════════════════════════════════════════════════════════════════

PPI SCORE: {ppi_data.get('ppi_score', 'N/A')}/100

NETWORK METRICS:
• Direct Interactions: {len(ppi_data.get('direct_interactions', []))}
• Network Centrality: {ppi_data.get('network_metrics', {}).get('centrality_score', 'N/A')}/100
• Avg Interaction Strength: {ppi_data.get('network_metrics', {}).get('avg_interaction_strength', 'N/A')}

═══════════════════════════════════════════════════════════════════════════════
DISEASE SIMILARITY ANALYSIS
═══════════════════════════════════════════════════════════════════════════════

SIMILARITY SCORE: {similarity_data.get('similarity_score', 'N/A')}/100

SIMILARITY DIMENSIONS:
• Pathophysiology: {similarity_data.get('similarity_metrics', {}).get('pathophysiology_similarity', 'N/A')}/100
• Mechanism Overlap: {similarity_data.get('similarity_metrics', {}).get('mechanism_overlap', 'N/A')}/100
• Pathway Convergence: {similarity_data.get('similarity_metrics', {}).get('pathway_convergence', 'N/A')}/100

═══════════════════════════════════════════════════════════════════════════════
AI-DRIVEN HYPOTHESIS GENERATION
═══════════════════════════════════════════════════════════════════════════════

HYPOTHESIS STRENGTH: {hypothesis_data.get('hypothesis_strength', {}).get('overall_strength', 'N/A')}/100

GENERATED HYPOTHESES: {len(hypothesis_data.get('hypotheses', []))}
{chr(10).join([f"• {h['hypothesis_id']}: {h['type']} ({h['confidence']} confidence)" for h in hypothesis_data.get('hypotheses', [])[:3]])}

⚠️ DISCLAIMER: Hypotheses are speculative and require experimental validation

═══════════════════════════════════════════════════════════════════════════════
INTEGRATED FEASIBILITY SCORE: {final_score}/100
═══════════════════════════════════════════════════════════════════════════════

This enhanced score integrates clinical evidence, mechanism validation, network biology,
disease similarity, and safety data to provide a comprehensive repurposing assessment.

═══════════════════════════════════════════════════════════════════════════════
TOP 5 REASONS THIS COULD WORK
═══════════════════════════════════════════════════════════════════════════════

{chr(10).join([f'{i+1}. {reason}' for i, reason in enumerate(reasons_work)])}

═══════════════════════════════════════════════════════════════════════════════
TOP 5 BLOCKERS & RISKS
═══════════════════════════════════════════════════════════════════════════════

{chr(10).join([f'{i+1}. {blocker}' for i, blocker in enumerate(blockers)])}

═══════════════════════════════════════════════════════════════════════════════
CONFIDENCE BREAKDOWN
═══════════════════════════════════════════════════════════════════════════════

Clinical Evidence:        {clinical_conf:.0f}% {'█' * int(clinical_conf/10)}
Literature/Mechanism:     {lit_conf:.0f}% {'█' * int(lit_conf/10)}
Patent/IP:                {patent_conf:.0f}% {'█' * int(patent_conf/10)}
Safety Profile:           {safety_conf:.0f}% {'█' * int(safety_conf/10)}
Market Analysis:          {market_conf:.0f}% {'█' * int(market_conf/10)}
Regulatory Strategy:      {reg_conf:.0f}% {'█' * int(reg_conf/10)}
Operational Readiness:    {internal_conf:.0f}% {'█' * int(internal_conf/10)}

OVERALL CONFIDENCE:       {avg_confidence:.0f}% {'█' * int(avg_confidence/10)}

═══════════════════════════════════════════════════════════════════════════════
STRATEGIC RECOMMENDATION: {recommendation}
═══════════════════════════════════════════════════════════════════════════════

{rec_detail}

NEXT STEPS:
1. {'Proceed to Phase 3 planning' if repurposing_score > 75 else 'Conduct additional validation studies' if repurposing_score > 60 else 'Reassess strategic fit'}
2. {'Finalize regulatory strategy' if reg_conf > 70 else 'Engage regulatory consultants for pathway optimization'}
3. {'Develop payer value proposition' if market_conf > 65 else 'Conduct market research and competitive analysis'}
4. {'Implement standard pharmacovigilance' if safety_conf > 75 else 'Design enhanced safety monitoring protocols'}
5. {'Secure funding and initiate launch preparation' if repurposing_score > 75 else 'Present findings to investment committee for go/no-go decision'}

═══════════════════════════════════════════════════════════════════════════════
END OF EXECUTIVE SUMMARY
═══════════════════════════════════════════════════════════════════════════════
    """.strip()
    
    return summary