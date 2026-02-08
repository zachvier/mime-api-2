import requests
import json
import auth

BASE_URL = "https://api.services.mimecast.com"

def get_all_managed_urls(token):
    """Fetches All Managed URLs."""
    print("Fetching Managed URLs...")
    api_url = f"{BASE_URL}/api/ttp/url/get-all-managed-urls"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api_url, headers=headers, json={})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching managed URLs: {e}")
        if e.response is not None:
             print(f"Response: {e.response.text}")
        return None

if __name__ == "__main__":
    token = auth.get_token()
    urls_data = get_all_managed_urls(token)

    if urls_data:
        print("\n--- Managed URLs Results ---")
        print(json.dumps(urls_data.get("data", []), indent=2))
