import os

import requests
from dotenv import load_dotenv

load_dotenv()

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")


def trigger_n8n_workflow(event_type: str, payload: dict) -> bool:
    """Dispatch event payloads to an n8n webhook for automated workflows."""
    if not N8N_WEBHOOK_URL:
        # Gracefully bypass if the n8n webhook URL is not configured.
        return False

    data = {
        "event": event_type,
        "payload": payload,
    }

    try:
        response = requests.post(N8N_WEBHOOK_URL, json=data, timeout=5)
        return response.status_code in [200, 201]
    except requests.exceptions.RequestException:
        # Non-blocking failure: logs can capture this in production.
        return False