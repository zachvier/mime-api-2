import requests
import json
import auth

BASE_URL = "https://api.services.mimecast.com"

def get_provisioning_packages(token):
    """Fetches Provisioning Packages."""
    print("Fetching Provisioning Packages...")
    api_url = f"{BASE_URL}/api/provisioning/get-packages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api_url, headers=headers, json={})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching packages: {e}")
        if e.response is not None:
             print(f"Response: {e.response.text}")
        return None

if __name__ == "__main__":
    token = auth.get_token()
    packages_data = get_provisioning_packages(token)

    if packages_data:
        print("\n--- Provisioning Packages Results ---")
        print(json.dumps(packages_data.get("data", []), indent=2))
