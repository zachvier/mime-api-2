import requests
import auth
from table_utils import print_records

BASE_URL = "https://api.services.mimecast.com"


def get_directory_connections(token):
    """Fetches directory connectors configured on the tenant."""
    print("Fetching directory connections...")
    api_url = f"{BASE_URL}/api/directory/get-connection"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    try:
        response = requests.post(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching directory connections: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
        return None


if __name__ == "__main__":
    token = auth.get_token()
    resp = get_directory_connections(token)

    if resp:
        rows = resp.get("data", []) or []
        print(f"\n--- Directory Connections ({len(rows)} entries) ---")
        if not rows:
            print("No directory connections returned.")
        else:
            print_records(rows)
