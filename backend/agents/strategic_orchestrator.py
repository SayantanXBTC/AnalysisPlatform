"""
Strategic Orchestrator - Enterprise-grade portfolio strategy AI
Dynamically assembles and executes agent workflows based on strategic intent
"""
from agents.prompt_intelligence_agent import PromptIntelligenceAgent
from agents.n8n_adapter_agent import N8NAdapterAgent
from agents.moa_agent import MoAAgent
from agents.ppi_agent import PPIAgent
from agents.disease_similarity_agent import DiseaseSimilarityAgent
from agents.hypothesis_agent import HypothesisAgent
from agents import clinical_agent, market_agent, patent_agent
from agents import regulatory_agent, safety_agent, internal_agent

try:
    from agents import literature_agent
    LITERATURE_AVAILABLE = True
except ImportError:
    LITERATURE_AVAILABLE = False

from datetime import datetime
from typing import Dict, List


class StrategicOrchestrator:
    """
    Portfolio strategy AI orchestrator
    Behaves like a strategic advisor, not a calculator
    """
    
    def __init__(self):
        self.prompt_intel = PromptIntelligenceAgent()
        self.n8n_adapter = N8NAdapterAgent()
        self.moa_agent = MoAAgent()
        self.ppi_agent = PPIAgent()
        self.similarity_agent = DiseaseSimilarityAgent()
        self.hypothesis_agent = HypothesisAgent()
    
    def process_strategic_prompt(self, prompt: str) -> Dict:
        """
        Main entry point: Process natural language strategic prompt
        
        Returns evidence-based strategic intelligence, NOT confidence percentages
        """
        print(f"\n{'='*80}")
        print(f"[Strategic Orchestrator] Processing prompt: {prompt}")
        print(f"{'='*80}\n")
        
        # Step 1: Parse prompt intelligence
        parsed = self.prompt_intel.parse_prompt(prompt)
        print(f"[Prompt Intelligence] Detected intents: {parsed['intents']}")
        print(f"[Prompt Intelligence] Query type: {parsed['query_type']}")
        print(f"[Prompt Intelligence] Entities: {parsed['entities']}")
        print(f"[Prompt Intelligence] Execution plan: {parsed['execution_plan']}\n")
        
        # Check if clarification needed
        clarification = self.prompt_intel.generate_clarification_prompt(parsed)
        if clarification:
            return {
                "status": "clarification_needed",
                "message": clarification,
                "original_prompt": prompt
            }
        
        # Step 2: Execute dynamic agent workflow
        intelligence = self._execute_workflow(parsed)
        
        # Step 3: Synthesize strategic narrative (NO PERCENTAGES)
        strategic_response = self._synthesize_strategic_response(
            prompt, parsed, intelligence
        )
        
        return strategic_response
    
    def _execute_workflow(self, parsed: Dict) -> Dict:
        """Execute dynamic agent workflow based on execution plan"""
        intelligence = {
            "parsed_prompt": parsed,
            "timestamp": datetime.now().isoformat()
        }
        
        plan = parsed["execution_plan"]
        entities = parsed["entities"]
        
        # Extract primary molecule/disease for agent calls
        primary_molecule = entities["molecules"][0] if entities["molecules"] else "Generic Molecule"
        primary_disease = entities["disease_areas"][0] if entities["disease_areas"] else "Target Indication"
        
        # Execute agents based on plan
        if "iqvia_market" in plan:
            print("[Orchestrator] Fetching IQVIA market intelligence...")
            intelligence["iqvia"] = self.n8n_adapter.fetch_iqvia_mock(primary_molecule, primary_disease)
        
        if "exim_trade" in plan:
            print("[Orchestrator] Fetching EXIM trade intelligence...")
            intelligence["exim"] = self.n8n_adapter.fetch_exim_mock(primary_molecule, primary_disease)
        
        if "clinical_trials" in plan:
            print("[Orchestrator] Analyzing clinical trial landscape...")
            intelligence["clinical"] = clinical_agent.analyze_clinical(primary_molecule, primary_disease)
        
        if "literature_review" in plan and LITERATURE_AVAILABLE:
            print("[Orchestrator] Reviewing scientific literature...")
            intelligence["literature"] = literature_agent.analyze_literature(primary_molecule, primary_disease)
        
        if "patent_landscape" in plan or "reformulation_opportunities" in plan:
            print("[Orchestrator] Analyzing patent landscape...")
            intelligence["patent"] = patent_agent.analyze_patent(primary_molecule, primary_disease)
        
        if "competitive_analysis" in plan or "market_analysis" in plan:
            print("[Orchestrator] Analyzing competitive landscape...")
            intelligence["market"] = market_agent.analyze_market(primary_molecule, primary_disease)
        
        if "safety_profile" in plan:
            print("[Orchestrator] Assessing safety profile...")
            intelligence["safety"] = safety_agent.analyze_safety(primary_molecule, primary_disease)
        
        if "moa_analysis" in plan:
            print("[Orchestrator] Analyzing mechanism of action...")
            intelligence["moa"] = self.moa_agent.run_moa(primary_molecule, primary_disease)
        
        if "ppi_network" in plan:
            print("[Orchestrator] Mapping protein interaction networks...")
            drug_targets = intelligence.get("moa", {}).get("primary_targets", [])
            intelligence["ppi"] = self.ppi_agent.run_ppi(drug_targets, [], primary_molecule, primary_disease)
        
        if "disease_similarity" in plan:
            print("[Orchestrator] Analyzing disease similarity...")
            intelligence["similarity"] = self.similarity_agent.run_similarity(primary_molecule, primary_disease)
        
        if "hypothesis_generation" in plan:
            print("[Orchestrator] Generating strategic hypotheses...")
            moa_data = intelligence.get("moa", {})
            ppi_data = intelligence.get("ppi", {})
            similarity_data = intelligence.get("similarity", {})
            evidence_features = self._extract_evidence_features(intelligence)
            intelligence["hypotheses"] = self.hypothesis_agent.run_hypothesis_engine(
                primary_molecule, primary_disease, moa_data, ppi_data, similarity_data, evidence_features
            )
        
        if "internal_rag" in plan:
            print("[Orchestrator] Querying internal knowledge base...")
            intelligence["internal"] = internal_agent.analyze_internal(primary_molecule, primary_disease)
        
        # Always include regulatory perspective if molecule-specific
        if entities["molecules"]:
            print("[Orchestrator] Assessing regulatory pathway...")
            intelligence["regulatory"] = regulatory_agent.analyze_regulatory(primary_molecule, primary_disease)
        
        return intelligence
    
    def _extract_evidence_features(self, intelligence: Dict) -> Dict:
        """Extract evidence quality features for hypothesis generation"""
        return {
            "clinical_confidence": intelligence.get("clinical", {}).get("confidence_score", 0.5),
            "literature_confidence": intelligence.get("literature", {}).get("confidence", 50) / 100,
            "safety_confidence": intelligence.get("safety", {}).get("confidence_score", 0.5),
            "market_confidence": intelligence.get("market", {}).get("confidence_score", 0.5)
        }
    
    def _synthesize_strategic_response(self, prompt: str, parsed: Dict, intelligence: Dict) -> Dict:
        """
        Synthesize strategic response with evidence-based classifications
        NO MISLEADING PERCENTAGES - Use qualitative bands instead
        """
        
        # Classify evidence strength (NOT percentage)
        evidence_strength = self._classify_evidence_strength(intelligence)
        
        # Classify innovation attractiveness
        innovation_attractiveness = self._classify_innovation_attractiveness(intelligence, parsed)
        
        # Classify scientific plausibility
        scientific_plausibility = self._classify_scientific_plausibility(intelligence)
        
        # Classify commercial feasibility
        commercial_feasibility = self._classify_commercial_feasibility(intelligence)
        
        # Generate executive narrative
        executive_narrative = self._generate_executive_narrative(
            prompt, parsed, intelligence, evidence_strength, 
            innovation_attractiveness, scientific_plausibility, commercial_feasibility
        )
        
        # Extract key insights
        key_insights = self._extract_key_insights(intelligence, parsed)
        
        # Identify risks and unknowns
        risks_unknowns = self._identify_risks_unknowns(intelligence)
        
        # Generate strategic recommendation
        strategic_recommendation = self._generate_strategic_recommendation(
            evidence_strength, innovation_attractiveness, scientific_plausibility, commercial_feasibility
        )
        
        # Suggest next steps (research-level only)
        next_steps = self._suggest_next_steps(parsed, intelligence, strategic_recommendation)
        
        return {
            "status": "success",
            "original_prompt": prompt,
            "query_type": parsed["query_type"],
            "timestamp": intelligence["timestamp"],
            
            # Strategic classifications (NO PERCENTAGES)
            "evidence_strength": evidence_strength,
            "innovation_attractiveness": innovation_attractiveness,
            "scientific_plausibility": scientific_plausibility,
            "commercial_feasibility": commercial_feasibility,
            
            # Narrative outputs
            "executive_summary": executive_narrative,
            "key_insights": key_insights,
            "risks_and_unknowns": risks_unknowns,
            "strategic_recommendation": strategic_recommendation,
            "suggested_next_steps": next_steps,
            
            # Detailed intelligence (for drill-down)
            "detailed_intelligence": self._format_detailed_intelligence(intelligence),
            
            # Metadata
            "agents_activated": parsed["execution_plan"],
            "entities_identified": parsed["entities"]
        }
    
    def _classify_evidence_strength(self, intelligence: Dict) -> str:
        """Classify overall evidence strength (NOT a percentage)"""
        
        # Count available evidence sources
        evidence_count = 0
        high_quality_count = 0
        
        if intelligence.get("clinical"):
            evidence_count += 1
            if intelligence["clinical"].get("total_trials", 0) > 10:
                high_quality_count += 1
        
        if intelligence.get("literature"):
            evidence_count += 1
            if intelligence["literature"].get("confidence", 0) > 70:
                high_quality_count += 1
        
        if intelligence.get("patent"):
            evidence_count += 1
        
        if intelligence.get("safety"):
            evidence_count += 1
        
        # Classify based on evidence availability and quality
        if high_quality_count >= 3:
            return "High"
        elif evidence_count >= 3 and high_quality_count >= 1:
            return "Moderate"
        elif evidence_count >= 2:
            return "Low"
        else:
            return "Very Low"
    
    def _classify_innovation_attractiveness(self, intelligence: Dict, parsed: Dict) -> str:
        """Classify innovation attractiveness"""
        
        # Check market opportunity signals
        market_signals = 0
        
        if intelligence.get("iqvia"):
            cagr = intelligence["iqvia"].get("cagr_percent", 0)
            if cagr > 10:
                market_signals += 2
            elif cagr > 5:
                market_signals += 1
        
        if intelligence.get("patent"):
            expiring_patents = intelligence["patent"].get("expiring_soon", 0)
            if expiring_patents > 0:
                market_signals += 1
        
        if intelligence.get("market"):
            competition = intelligence["market"].get("competitive_density", "high")
            if competition == "low":
                market_signals += 2
            elif competition == "moderate":
                market_signals += 1
        
        # Classify
        if market_signals >= 4:
            return "Strong"
        elif market_signals >= 2:
            return "Promising"
        else:
            return "Weak"
    
    def _classify_scientific_plausibility(self, intelligence: Dict) -> str:
        """Classify scientific plausibility"""
        
        # Check mechanistic support
        moa_score = intelligence.get("moa", {}).get("moa_score", 0)
        ppi_score = intelligence.get("ppi", {}).get("ppi_score", 0)
        similarity_score = intelligence.get("similarity", {}).get("similarity_score", 0)
        
        avg_mechanistic = (moa_score + ppi_score + similarity_score) / 3 if moa_score else 0
        
        if avg_mechanistic >= 75:
            return "Mechanistically Supported"
        elif avg_mechanistic >= 50:
            return "Hypothesis-Level"
        else:
            return "Unsupported"
    
    def _classify_commercial_feasibility(self, intelligence: Dict) -> str:
        """Classify commercial feasibility"""
        
        # Check market and regulatory factors
        feasibility_score = 0
        
        if intelligence.get("market"):
            market_conf = intelligence["market"].get("confidence_score", 0)
            if market_conf > 0.7:
                feasibility_score += 2
            elif market_conf > 0.5:
                feasibility_score += 1
        
        if intelligence.get("patent"):
            patent_conf = intelligence["patent"].get("confidence_score", 0)
            if patent_conf > 0.7:
                feasibility_score += 1
        
        if intelligence.get("regulatory"):
            reg_conf = intelligence["regulatory"].get("confidence_score", 0)
            if reg_conf > 0.7:
                feasibility_score += 1
        
        if feasibility_score >= 3:
            return "High"
        elif feasibility_score >= 2:
            return "Medium"
        else:
            return "Low"
    
    def _generate_executive_narrative(self, prompt, parsed, intelligence, 
                                     evidence_strength, innovation_attractiveness,
                                     scientific_plausibility, commercial_feasibility) -> str:
        """Generate executive-level strategic narrative"""
        
        entities = parsed["entities"]
        query_type = parsed["query_type"]
        
        # Build context
        if entities["molecules"]:
            context = f"Analysis of {', '.join(entities['molecules'])}"
        elif entities["disease_areas"]:
            context = f"Strategic exploration of {', '.join(entities['disease_areas'])} therapeutic area"
        else:
            context = "Portfolio strategy analysis"
        
        narrative = f"""
**{context}**

**Query Intent**: {query_type.replace('_', ' ').title()}

**Evidence Assessment**:
• Evidence Strength: {evidence_strength}
• Scientific Plausibility: {scientific_plausibility}
• Innovation Attractiveness: {innovation_attractiveness}
• Commercial Feasibility: {commercial_feasibility}

**Strategic Context**:
{self._build_strategic_context(intelligence, parsed)}

**Key Considerations**:
{self._build_key_considerations(intelligence, evidence_strength)}
        """.strip()
        
        return narrative
    
    def _build_strategic_context(self, intelligence: Dict, parsed: Dict) -> str:
        """Build strategic context paragraph"""
        
        context_points = []
        
        # Clinical context
        if intelligence.get("clinical"):
            trials = intelligence["clinical"].get("total_trials", 0)
            if trials > 0:
                context_points.append(f"{trials} clinical trials identified in relevant therapeutic areas")
        
        # Market context
        if intelligence.get("iqvia"):
            market_size = intelligence["iqvia"].get("market_size_usd_millions", 0)
            if market_size > 0:
                context_points.append(f"Market size estimated at ${market_size}M with observable growth trends")
        
        # Patent context
        if intelligence.get("patent"):
            patents = intelligence["patent"].get("total_patents", 0)
            if patents > 0:
                context_points.append(f"{patents} relevant patents identified in IP landscape")
        
        if not context_points:
            return "Limited direct evidence available in current datasets. Analysis based on therapeutic area patterns and mechanistic rationale."
        
        return " • ".join(context_points)
    
    def _build_key_considerations(self, intelligence: Dict, evidence_strength: str) -> str:
        """Build key considerations based on evidence"""
        
        considerations = []
        
        if evidence_strength in ["Very Low", "Low"]:
            considerations.append("⚠️ Limited direct evidence - conclusions are exploratory")
        
        if intelligence.get("safety"):
            signals = intelligence["safety"].get("total_safety_signals", 0)
            if signals > 5:
                considerations.append("⚠️ Notable safety signals require careful evaluation")
        
        if intelligence.get("hypotheses"):
            considerations.append("💡 AI-generated hypotheses require experimental validation")
        
        if not considerations:
            considerations.append("✓ Evidence base supports further strategic evaluation")
        
        return "\n".join(considerations)
    
    def _extract_key_insights(self, intelligence: Dict, parsed: Dict) -> List[str]:
        """Extract key strategic insights"""
        insights = []
        
        # Add insights from each agent
        for agent_name, agent_data in intelligence.items():
            if isinstance(agent_data, dict) and "key_findings" in agent_data:
                insights.extend(agent_data["key_findings"][:2])  # Top 2 from each
        
        return insights[:8]  # Max 8 insights
    
    def _identify_risks_unknowns(self, intelligence: Dict) -> List[str]:
        """Identify risks and knowledge gaps"""
        risks = []
        
        # Check for missing evidence
        if not intelligence.get("clinical"):
            risks.append("No clinical trial data available - efficacy unvalidated")
        
        if not intelligence.get("safety"):
            risks.append("Safety profile not fully characterized")
        
        # Check for uncertainty flags
        if intelligence.get("hypotheses"):
            uncertainty_flags = intelligence["hypotheses"].get("uncertainty_flags", [])
            for flag in uncertainty_flags[:3]:
                risks.append(f"{flag.get('flag', 'Unknown risk')}")
        
        return risks
    
    def _generate_strategic_recommendation(self, evidence_strength, innovation_attractiveness,
                                          scientific_plausibility, commercial_feasibility) -> Dict:
        """Generate strategic recommendation (NOT a percentage)"""
        
        # Decision logic based on qualitative classifications
        if (evidence_strength in ["High", "Moderate"] and 
            innovation_attractiveness in ["Strong", "Promising"] and
            scientific_plausibility == "Mechanistically Supported"):
            
            return {
                "classification": "Worth Pursuing",
                "rationale": "Strong evidence base, attractive market opportunity, and solid scientific rationale support further investment.",
                "confidence_band": "High Confidence"
            }
        
        elif (evidence_strength in ["Moderate", "Low"] and
              innovation_attractiveness in ["Promising", "Strong"]):
            
            return {
                "classification": "Requires Validation",
                "rationale": "Market opportunity exists but evidence gaps require targeted research before major investment.",
                "confidence_band": "Moderate Confidence"
            }
        
        else:
            return {
                "classification": "High Risk / Exploratory",
                "rationale": "Significant uncertainties and limited evidence. Consider only for early-stage exploration.",
                "confidence_band": "Low Confidence"
            }
    
    def _suggest_next_steps(self, parsed: Dict, intelligence: Dict, recommendation: Dict) -> List[str]:
        """Suggest research-level next steps (NOT clinical recommendations)"""
        
        steps = []
        
        if recommendation["classification"] == "Worth Pursuing":
            steps.append("Conduct detailed competitive intelligence and market sizing")
            steps.append("Engage regulatory consultants for pathway optimization")
            steps.append("Develop comprehensive development timeline and budget")
        
        elif recommendation["classification"] == "Requires Validation":
            steps.append("Commission targeted literature review and expert consultation")
            steps.append("Conduct preliminary market research and payer interviews")
            steps.append("Evaluate preclinical validation requirements")
        
        else:
            steps.append("Monitor therapeutic area for emerging evidence")
            steps.append("Consider alternative indications or formulations")
            steps.append("Reassess if new clinical data becomes available")
        
        return steps
    
    def _format_detailed_intelligence(self, intelligence: Dict) -> Dict:
        """Format detailed intelligence for drill-down"""
        
        formatted = {}
        
        # Only include non-empty agent outputs
        for key, value in intelligence.items():
            if key not in ["parsed_prompt", "timestamp"] and value:
                formatted[key] = value
        
        return formatted
