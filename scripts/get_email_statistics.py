import requests
import auth
from table_utils import print_records

BASE_URL = "https://api.services.mimecast.com"


def get_email_statistics(token):
    """Fetches Cloud Gateway email statistics."""
    print("Fetching Email Statistics...")
    api_url = f"{BASE_URL}/email/cloud-gateway/v1/statistics"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching email statistics: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
        return None


if __name__ == "__main__":
    token = auth.get_token()
    stats_data = get_email_statistics(token)

    if stats_data:
        print("\n--- Email Statistics ---")
        if isinstance(stats_data, dict) and "data" in stats_data:
            rows = stats_data.get("data") or []
        elif isinstance(stats_data, list):
            rows = stats_data
        else:
            rows = [stats_data]
        print_records(rows)
