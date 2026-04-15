import requests
import json
import auth
from table_utils import print_records

BASE_URL = "https://api.services.mimecast.com"

def get_internal_domains(token):
    """Fetches the list of internal domains on the account."""
    print("Fetching internal domains...")
    api_url = f"{BASE_URL}/api/domain/get-internal-domain"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {"data": []}

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching internal domains: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
        return None

if __name__ == "__main__":
    token = auth.get_token()
    resp = get_internal_domains(token)

    if resp:
        data = resp.get("data", [])
        rows = []
        for block in data:
            if isinstance(block, dict) and "domains" in block:
                rows.extend(block["domains"])
            else:
                rows.append(block)
        print(f"\n--- Internal Domains ({len(rows)} entries) ---")
        if not rows:
            print("No domains returned.")
        else:
            print_records(rows)
