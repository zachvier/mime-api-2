import requests
import json
from datetime import datetime, timedelta, timezone
import auth

BASE_URL = "https://api.services.mimecast.com"

def get_ttp_attachment_logs(token):
    """Fetches TTP Attachment Protection Logs for the last 7 days."""
    print("Fetching TTP Attachment Logs...")
    api_url = f"{BASE_URL}/api/ttp/attachment/get-logs"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    now = datetime.now(timezone.utc)
    start = now - timedelta(days=7)
    fmt = "%Y-%m-%dT%H:%M:%SZ"

    payload = {
        "data": [{
            "from": start.strftime(fmt),
            "to": now.strftime(fmt)
        }]
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching TTP attachment logs: {e}")
        if e.response is not None:
             print(f"Response: {e.response.text}")
        return None

if __name__ == "__main__":
    token = auth.get_token()
    logs_data = get_ttp_attachment_logs(token)

    if logs_data:
        print("\n--- TTP Attachment Logs Results ---")
        print(json.dumps(logs_data.get("data", []), indent=2))
