import uuid
import os
import requests

def generate_report_id():
    return str(uuid.uuid4())

def ensure_reports_dir():
    os.makedirs("reports", exist_ok=True)

def send_to_n8n(url: str, payload: dict):
    """Send webhook notification to n8n"""
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        print(f"[SUCCESS] n8n webhook sent to {url}")
        return True
    except Exception as e:
        print(f"[ERROR n8n] Failed to send webhook: {e}")
        return False