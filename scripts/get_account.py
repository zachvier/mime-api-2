import requests
import json
import auth
from table_utils import print_records

BASE_URL = "https://api.services.mimecast.com"

def get_account_info(token):
    """Fetches Account Information."""
    print("Fetching Account Info...")
    api_url = f"{BASE_URL}/api/account/get-account"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(api_url, headers=headers, json={})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching account info: {e}")
        if e.response is not None:
             print(f"Response: {e.response.text}")
        return None

if __name__ == "__main__":
    token = auth.get_token()
    account_data = get_account_info(token)
    
    if account_data:
        data = account_data.get("data", [])
        print("\n--- Account Info ---")
        if not data:
            print("No account info returned.")
        else:
            print_records(data)
