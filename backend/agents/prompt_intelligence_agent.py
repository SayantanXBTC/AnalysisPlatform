"""
Prompt Intelligence Agent - Parses natural language strategic prompts
Extracts intent, entities, geography, population, and strategic objectives
"""
import re
from typing import Dict, List, Optional


class PromptIntelligenceAgent:
    """
    Intelligent prompt parser for pharmaceutical portfolio strategy queries
    Transforms free-form natural language into structured execution plans
    """
    
    def __init__(self):
        # Strategic intent patterns
        self.intent_patterns = {
            "market_opportunity": [
                r"market opportunity", r"low competition", r"high unmet need",
                r"market gap", r"whitespace", r"underserved", r"market saturation"
            ],
            "repurposing": [
                r"repurpos", r"new indication", r"alternative use",
                r"expand indication", r"off-label"
            ],
            "patent_cliff": [
                r"patent expir", r"patent cliff", r"off-patent",
                r"generic entry", r"exclusivity end"
            ],
            "reformulation": [
                r"reformulat", r"new formulation", r"delivery system",
                r"dosage form", r"value-added"
            ],
            "trade_risk": [
                r"supply chain", r"trade", r"import", r"export",
                r"sourcing", r"supply risk"
            ],
            "innovation": [
                r"innovation", r"differentiat", r"novel",
                r"first-in-class", r"best-in-class"
            ],
            "competitive_analysis": [
                r"competitor", r"competitive landscape", r"market share",
                r"competition"
            ]
        }
        
        # Disease area patterns
        self.disease_areas = {
            "cardiovascular": ["cardiovascular", "cardiac", "heart", "hypertension", "cvd"],
            "respiratory": ["respiratory", "asthma", "copd", "pulmonary", "lung"],
            "oncology": ["cancer", "oncology", "tumor", "malignancy", "carcinoma"],
            "cns": ["cns", "neurological", "alzheimer", "parkinson", "depression", "anxiety"],
            "metabolic": ["diabetes", "metabolic", "obesity", "thyroid"],
            "inflammatory": ["inflammatory", "arthritis", "autoimmune", "rheumatoid"],
            "infectious": ["infectious", "antibiotic", "antiviral", "antimicrobial"],
            "gastrointestinal": ["gastrointestinal", "gi", "digestive", "ibd", "crohn"],
            "dermatology": ["dermatology", "skin", "psoriasis", "eczema"],
            "pediatric": ["pediatric", "children", "infant", "neonatal"]
        }
        
        # Geography patterns
        self.geographies = {
            "india": ["india", "indian"],
            "us": ["us", "usa", "united states", "america"],
            "europe": ["europe", "eu", "european"],
            "china": ["china", "chinese"],
            "japan": ["japan", "japanese"],
            "emerging": ["emerging market", "developing", "brics"]
        }
        
        # Population patterns
        self.populations = {
            "pediatric": ["pediatric", "children", "child", "infant", "neonatal"],
            "geriatric": ["geriatric", "elderly", "senior", "aged"],
            "women": ["women", "female", "maternal"],
            "rare_disease": ["rare disease", "orphan", "ultra-rare"]
        }
        
        # Drug class patterns
        self.drug_classes = {
            "anti-inflammatory": ["anti-inflammatory", "nsaid", "corticosteroid"],
            "antibiotic": ["antibiotic", "antimicrobial", "antibacterial"],
            "antihypertensive": ["antihypertensive", "ace inhibitor", "beta blocker"],
            "antidiabetic": ["antidiabetic", "insulin", "metformin"],
            "immunosuppressant": ["immunosuppressant", "immunomodulator"],
            "chemotherapy": ["chemotherapy", "cytotoxic", "antineoplastic"]
        }
    
    def parse_prompt(self, prompt: str) -> Dict:
        """
        Parse natural language prompt into structured intelligence
        
        Returns:
            {
                "original_prompt": str,
                "intents": List[str],
                "entities": {
                    "molecules": List[str],
                    "disease_areas": List[str],
                    "drug_classes": List[str],
                    "geographies": List[str],
                    "populations": List[str]
                },
                "execution_plan": List[str],
                "query_type": str,
                "confidence": str
            }
        """
        prompt_lower = prompt.lower()
        
        # Extract intents
        intents = self._extract_intents(prompt_lower)
        
        # Extract entities
        entities = {
            "molecules": self._extract_molecules(prompt),
            "disease_areas": self._extract_disease_areas(prompt_lower),
            "drug_classes": self._extract_drug_classes(prompt_lower),
            "geographies": self._extract_geographies(prompt_lower),
            "populations": self._extract_populations(prompt_lower)
        }
        
        # Determine query type
        query_type = self._determine_query_type(intents, entities)
        
        # Build execution plan
        execution_plan = self._build_execution_plan(intents, entities, query_type)
        
        # Assess parsing confidence
        confidence = self._assess_confidence(intents, entities)
        
        return {
            "original_prompt": prompt,
            "intents": intents,
            "entities": entities,
            "execution_plan": execution_plan,
            "query_type": query_type,
            "confidence": confidence,
            "requires_clarification": len(intents) == 0 and len(entities["disease_areas"]) == 0
        }
    
    def _extract_intents(self, prompt: str) -> List[str]:
        """Extract strategic intents from prompt"""
        detected_intents = []
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, prompt):
                    detected_intents.append(intent)
                    break
        
        return list(set(detected_intents))
    
    def _extract_molecules(self, prompt: str) -> List[str]:
        """Extract specific molecule names (capitalized words)"""
        # Look for capitalized words that might be drug names
        words = prompt.split()
        molecules = []
        
        for word in words:
            # Remove punctuation
            clean_word = re.sub(r'[^\w\s]', '', word)
            # Check if it's capitalized and longer than 3 chars
            if clean_word and clean_word[0].isupper() and len(clean_word) > 3:
                # Exclude common words
                if clean_word.lower() not in ['which', 'what', 'where', 'when', 'india', 'china', 'europe']:
                    molecules.append(clean_word)
        
        return molecules
    
    def _extract_disease_areas(self, prompt: str) -> List[str]:
        """Extract disease areas from prompt"""
        detected_areas = []
        
        for area, keywords in self.disease_areas.items():
            for keyword in keywords:
                if keyword in prompt:
                    detected_areas.append(area)
                    break
        
        return list(set(detected_areas))
    
    def _extract_drug_classes(self, prompt: str) -> List[str]:
        """Extract drug classes from prompt"""
        detected_classes = []
        
        for drug_class, keywords in self.drug_classes.items():
            for keyword in keywords:
                if keyword in prompt:
                    detected_classes.append(drug_class)
                    break
        
        return list(set(detected_classes))
    
    def _extract_geographies(self, prompt: str) -> List[str]:
        """Extract geographic regions from prompt"""
        detected_geos = []
        
        for geo, keywords in self.geographies.items():
            for keyword in keywords:
                if keyword in prompt:
                    detected_geos.append(geo)
                    break
        
        return list(set(detected_geos))
    
    def _extract_populations(self, prompt: str) -> List[str]:
        """Extract target populations from prompt"""
        detected_pops = []
        
        for pop, keywords in self.populations.items():
            for keyword in keywords:
                if keyword in prompt:
                    detected_pops.append(pop)
                    break
        
        return list(set(detected_pops))
    
    def _determine_query_type(self, intents: List[str], entities: Dict) -> str:
        """Determine the primary query type"""
        
        # Specific molecule query
        if entities["molecules"]:
            return "molecule_specific"
        
        # Disease area exploration
        if entities["disease_areas"] and not entities["molecules"]:
            return "disease_area_exploration"
        
        # Drug class analysis
        if entities["drug_classes"]:
            return "drug_class_analysis"
        
        # Market opportunity scan
        if "market_opportunity" in intents:
            return "market_opportunity_scan"
        
        # Patent cliff analysis
        if "patent_cliff" in intents:
            return "patent_cliff_analysis"
        
        # Repurposing exploration
        if "repurposing" in intents:
            return "repurposing_exploration"
        
        # If no specific intent but has entities, do comprehensive analysis
        if entities["disease_areas"] or entities["drug_classes"] or entities["geographies"]:
            return "comprehensive_analysis"
        
        # Default to strategic exploration (works for ANY prompt)
        return "strategic_exploration"
    
    def _build_execution_plan(self, intents: List[str], entities: Dict, query_type: str) -> List[str]:
        """Build dynamic agent execution plan based on parsed intelligence"""
        plan = []
        
        # Always start with prompt classification
        plan.append("prompt_classification")
        
        # For ANY prompt, run comprehensive analysis
        # This ensures all agents work regardless of prompt specificity
        
        # Market opportunity queries
        if "market_opportunity" in intents or query_type == "market_opportunity_scan":
            plan.extend(["iqvia_market", "exim_trade", "competitive_analysis"])
        
        # Repurposing queries
        if "repurposing" in intents or query_type == "repurposing_exploration":
            plan.extend(["clinical_trials", "literature_review", "moa_analysis", 
                        "ppi_network", "disease_similarity"])
        
        # Patent cliff queries
        if "patent_cliff" in intents or query_type == "patent_cliff_analysis":
            plan.extend(["patent_landscape", "market_analysis", "reformulation_opportunities"])
        
        # Innovation/differentiation queries
        if "innovation" in intents or "reformulation" in intents:
            plan.extend(["patent_landscape", "moa_analysis", "competitive_analysis"])
        
        # Trade/supply risk queries
        if "trade_risk" in intents:
            plan.extend(["exim_trade", "supply_chain_analysis"])
        
        # Comprehensive analysis - run ALL agents for complete intelligence
        if query_type in ["comprehensive_analysis", "strategic_exploration"] or len(plan) <= 1:
            plan.extend([
                "clinical_trials",
                "literature_review",
                "iqvia_market",
                "exim_trade",
                "patent_landscape",
                "moa_analysis",
                "ppi_network",
                "disease_similarity",
                "competitive_analysis",
                "safety_profile",
                "hypothesis_generation"
            ])
        
        # Always include safety if molecules are mentioned
        if entities["molecules"] and "safety_profile" not in plan:
            plan.append("safety_profile")
        
        # Always include hypothesis generation for strategic queries
        if query_type in ["repurposing_exploration", "strategic_exploration", "comprehensive_analysis"]:
            if "hypothesis_generation" not in plan:
                plan.append("hypothesis_generation")
        
        # Always check internal knowledge
        plan.append("internal_rag")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_plan = []
        for item in plan:
            if item not in seen:
                seen.add(item)
                unique_plan.append(item)
        
        return unique_plan
    
    def _assess_confidence(self, intents: List[str], entities: Dict) -> str:
        """Assess parsing confidence"""
        
        # High confidence: clear intent + specific entities
        if len(intents) >= 1 and (entities["molecules"] or entities["disease_areas"]):
            return "high"
        
        # Moderate confidence: intent or entities present
        if len(intents) >= 1 or entities["disease_areas"] or entities["drug_classes"]:
            return "moderate"
        
        # Accept ANY prompt - even vague ones get moderate confidence
        # System will run comprehensive analysis
        return "moderate"
    
    def generate_clarification_prompt(self, parsed: Dict) -> Optional[str]:
        """Generate clarification question if prompt is too vague"""
        
        # NEVER require clarification - accept ANY prompt
        # System will run comprehensive analysis for all queries
        return None
