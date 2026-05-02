import requests
import auth
from table_utils import print_records

BASE_URL = "https://api.services.mimecast.com"


def get_gateway_details(token):
    """Fetches Cloud Gateway details."""
    print("Fetching Gateway Details...")
    api_url = f"{BASE_URL}/email/cloud-gateway/v1/gateway-details"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching gateway details: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
        return None


if __name__ == "__main__":
    token = auth.get_token()
    gateway_data = get_gateway_details(token)

    if gateway_data:
        print("\n--- Gateway Details ---")
        if isinstance(gateway_data, dict) and "data" in gateway_data:
            rows = gateway_data.get("data") or []
        elif isinstance(gateway_data, list):
            rows = gateway_data
        else:
            rows = [gateway_data]
        print_records(rows)
