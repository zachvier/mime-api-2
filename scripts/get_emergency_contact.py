import requests
import json
import auth
import sys
from table_utils import print_records

BASE_URL = "https://api.services.mimecast.com"

def get_emergency_contact(token):
    """Fetches Emergency Contact Information."""
    print("Fetching Emergency Contact Info...")
    api_url = f"{BASE_URL}/account/cloud-gateway/v1/emergency-contact"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching emergency contact info: {e}")
        if e.response is not None:
             print(f"Response: {e.response.text}")
        return None

if __name__ == "__main__":
    token = auth.get_token()
    contact_data = get_emergency_contact(token)
    
    if contact_data:
        print("\n--- Emergency Contact ---")
        if isinstance(contact_data, dict) and "data" in contact_data:
            rows = contact_data.get("data") or []
        elif isinstance(contact_data, list):
            rows = contact_data
        else:
            rows = [contact_data]
        print_records(rows)
