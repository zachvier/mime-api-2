import requests
import auth
from table_utils import print_records

BASE_URL = "https://api.services.mimecast.com"


def get_outbound_ip_addresses(token):
    """Fetches Cloud Gateway outbound IP addresses."""
    print("Fetching Outbound IP Addresses...")
    api_url = f"{BASE_URL}/email/cloud-gateway/v1/outbound-ip-addresses"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching outbound IP addresses: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
        return None


if __name__ == "__main__":
    token = auth.get_token()
    ip_data = get_outbound_ip_addresses(token)

    if ip_data:
        print("\n--- Outbound IP Addresses ---")
        if isinstance(ip_data, dict) and "data" in ip_data:
            rows = ip_data.get("data") or []
        elif isinstance(ip_data, list):
            rows = ip_data
        else:
            rows = [ip_data]
        print_records(rows)
