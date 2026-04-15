import requests
import json
import auth
import sys
from table_utils import print_records

BASE_URL = "https://api.services.mimecast.com"

def get_whoami(token, account_code=None):
    """Fetches Identity Whoami Information."""
    print("Fetching Identity Information (whoami)...")
    api_url = f"{BASE_URL}/identity/whoami"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    if account_code:
        headers["x-mc-accountcode"] = account_code
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching identity info: {e}")
        if e.response is not None:
             print(f"Response: {e.response.text}")
        return None

if __name__ == "__main__":
    token = auth.get_token()
    config = auth.get_config()
    account_code = config.get("account_code")
    
    whoami_data = get_whoami(token, account_code)
    
    if whoami_data:
        print("\n--- Identity Whoami ---")
        if isinstance(whoami_data, dict) and "data" in whoami_data:
            rows = whoami_data.get("data") or []
        elif isinstance(whoami_data, list):
            rows = whoami_data
        else:
            rows = [whoami_data]
        print_records(rows)
