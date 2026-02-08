import requests
import json
import auth

BASE_URL = "https://api.services.mimecast.com"

def get_audit_categories(token):
    """Fetches Audit Event Categories."""
    print("Fetching Audit Categories...")
    api_url = f"{BASE_URL}/api/audit/get-categories"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api_url, headers=headers, json={})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching audit categories: {e}")
        if e.response is not None:
             print(f"Response: {e.response.text}")
        return None

if __name__ == "__main__":
    token = auth.get_token()
    categories_data = get_audit_categories(token)

    if categories_data:
        categories = categories_data.get("data", [{}])[0].get("categories", [])
        categories.sort(key=lambda c: c.get("id", 0))
        print("\n--- Audit Categories Results ---")
        print(json.dumps(categories, indent=2))
