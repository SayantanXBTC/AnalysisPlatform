"""
n8n Adapter Agent - Fetches mock data from IQVIA and EXIM via n8n webhooks
"""
import requests
import hashlib
from config import N8N_IQVIA_URL, N8N_EXIM_URL


class N8NAdapterAgent:
    """Agent to fetch mock IQVIA and EXIM data via n8n webhooks"""
    
    def __init__(self):
        self.iqvia_url = N8N_IQVIA_URL
        self.exim_url = N8N_EXIM_URL
    
    def fetch_iqvia_mock(self, drug_name: str, indication: str):
        """Fetch IQVIA mock market data via n8n webhook"""
        try:
            # Try to fetch from n8n webhook
            payload = {"drug": drug_name, "indication": indication}
            res = requests.post(self.iqvia_url, json=payload, timeout=10)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            print(f"[WARN] IQVIA mock fetch failed: {e}, using fallback data")
            # Fallback to synthetic data
            return self._generate_iqvia_fallback(drug_name, indication)
    
    def fetch_exim_mock(self, drug_name: str, indication: str):
        """Fetch EXIM trade data via n8n webhook"""
        try:
            # Try to fetch from n8n webhook
            payload = {"drug": drug_name, "indication": indication}
            res = requests.post(self.exim_url, json=payload, timeout=10)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            print(f"[WARN] EXIM mock fetch failed: {e}, using fallback data")
            # Fallback to synthetic data
            return self._generate_exim_fallback(drug_name, indication)
    
    def _generate_iqvia_fallback(self, drug_name: str, indication: str):
        """Generate synthetic IQVIA market intelligence data"""
        seed = int(hashlib.md5(f"{drug_name}{indication}".encode()).hexdigest(), 16) % 10000
        
        market_size = 500 + (seed % 5000)
        growth_rate = 3.5 + (seed % 15)
        market_share = 5 + (seed % 30)
        
        return {
            "section": "IQVIA Market Intelligence",
            "data_source": "IQVIA Mock API (Fallback)",
            "market_size_usd_millions": market_size,
            "cagr_percent": round(growth_rate, 1),
            "current_market_share_percent": round(market_share, 1),
            "top_competitors": [
                {"name": "Competitor A", "market_share": 25.3},
                {"name": "Competitor B", "market_share": 18.7},
                {"name": "Competitor C", "market_share": 15.2}
            ],
            "regional_breakdown": {
                "North America": 45,
                "Europe": 30,
                "Asia Pacific": 20,
                "Rest of World": 5
            },
            "forecast_2025": market_size * 1.15,
            "forecast_2030": market_size * 1.45,
            "key_insights": [
                f"Market size estimated at ${market_size}M with {growth_rate:.1f}% CAGR",
                f"Current market share opportunity: {market_share:.1f}%",
                "Strong growth in emerging markets",
                "Increasing demand for innovative therapies"
            ],
            "confidence_score": 0.65,
            "quality_notes": "Synthetic IQVIA-style market data (n8n webhook unavailable)"
        }
    
    def _generate_exim_fallback(self, drug_name: str, indication: str):
        """Generate synthetic EXIM trade data"""
        seed = int(hashlib.md5(f"{drug_name}{indication}exim".encode()).hexdigest(), 16) % 10000
        
        export_value = 50 + (seed % 500)
        import_value = 30 + (seed % 300)
        
        return {
            "section": "EXIM Trade Intelligence",
            "data_source": "EXIM Mock API (Fallback)",
            "total_exports_usd_millions": export_value,
            "total_imports_usd_millions": import_value,
            "trade_balance_usd_millions": export_value - import_value,
            "top_export_destinations": [
                {"country": "United States", "value_usd_millions": export_value * 0.35},
                {"country": "Germany", "value_usd_millions": export_value * 0.25},
                {"country": "United Kingdom", "value_usd_millions": export_value * 0.20}
            ],
            "top_import_sources": [
                {"country": "China", "value_usd_millions": import_value * 0.40},
                {"country": "India", "value_usd_millions": import_value * 0.30},
                {"country": "Switzerland", "value_usd_millions": import_value * 0.20}
            ],
            "trade_trends": {
                "export_growth_yoy_percent": 8.5 + (seed % 10),
                "import_growth_yoy_percent": 6.2 + (seed % 8),
                "trade_balance_trend": "Positive" if export_value > import_value else "Negative"
            },
            "key_insights": [
                f"Total pharmaceutical exports: ${export_value}M",
                f"Trade balance: ${export_value - import_value}M {'surplus' if export_value > import_value else 'deficit'}",
                "Strong export growth in developed markets",
                "Increasing import competition from Asia"
            ],
            "confidence_score": 0.60,
            "quality_notes": "Synthetic EXIM-style trade data (n8n webhook unavailable)"
        }
