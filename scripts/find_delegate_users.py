import requests
import auth
from table_utils import print_records

BASE_URL = "https://api.services.mimecast.com"


def find_delegate_users(token, primary_address):
    """Fetches delegate users for a primary address."""
    api_url = f"{BASE_URL}/api/user/find-delegate-users"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {"data": [{"primaryAddress": primary_address}]}

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error finding delegate users: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
        return None


if __name__ == "__main__":
    token = auth.get_token()

    primary_address = input("\nEnter primary email address: ").strip()
    if not primary_address:
        print("Primary email address is required.")
        raise SystemExit(1)

    print(f"\n{'='*50}")
    print(f"Primary address: {primary_address}")
    print(f"{'='*50}\n")

    resp = find_delegate_users(token, primary_address)
    if not resp:
        raise SystemExit(1)

    delegates = []
    for block in resp.get("data", []) or []:
        if isinstance(block, dict) and "delegateUsers" in block:
            delegates.extend(block["delegateUsers"])

    print(f"--- Delegate Users for {primary_address} ({len(delegates)} total) ---")
    if delegates:
        print_records(delegates)
    else:
        print("No delegate users found.")

    fails = resp.get("fail", []) or []
    if fails:
        print("\n--- Failures ---")
        for f in fails:
            for err in f.get("errors", []):
                print(f"  {err.get('code')}: {err.get('message')}")
