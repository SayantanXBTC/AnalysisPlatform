import uuid
import os

def generate_report_id():
    return str(uuid.uuid4())

def ensure_reports_dir():
    os.makedirs("reports", exist_ok=True)