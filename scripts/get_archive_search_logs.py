import requests
import json
import auth
import sys
from table_utils import print_records

BASE_URL = "https://api.services.mimecast.com"

def get_archive_search_logs(token, page_size=25):
    """Fetches Archive Search Logs."""
    print(f"Fetching Archive Search Logs (Page Size: {page_size})...")
    api_url = f"{BASE_URL}/api/archive/get-archive-search-logs"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "meta": {
            "pagination": {
                "pageSize": page_size
            }
        },
        "data": []
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching archive search logs: {e}")
        if e.response is not None:
             print(f"Response: {e.response.text}")
        return None

if __name__ == "__main__":
    token = auth.get_token()
    logs_data = get_archive_search_logs(token)
    
    if logs_data:
        rows = []
        for block in logs_data.get("data", []):
            rows.extend(block.get("logs", []))
        print(f"\n--- Archive Search Logs ({len(rows)} total) ---")
        if not rows:
            print("No search logs found.")
        else:
            print_records(rows)
        
        # Check for more pages
        meta = logs_data.get("meta", {})
        pagination = meta.get("pagination", {})
        next_token = pagination.get("next")
        if next_token:
            print(f"\nNext Page Token: {next_token}")
