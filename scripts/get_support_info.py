import requests
import json
import auth
from table_utils import print_records

BASE_URL = "https://api.services.mimecast.com"

def get_support_info(token):
    """Fetches Account Support Info."""
    print("Fetching Support Info...")
    api_url = f"{BASE_URL}/api/account/get-support-info"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(api_url, headers=headers, json={})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching support info: {e}")
        if e.response is not None:
             print(f"Response: {e.response.text}")
        return None

if __name__ == "__main__":
    token = auth.get_token()
    support_data = get_support_info(token)
    
    if support_data:
        data = support_data.get("data", [])
        print("\n--- Support Info ---")
        if not data:
            print("No support info returned.")
        else:
            print_records(data)
