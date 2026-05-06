import requests
import auth
from table_utils import print_records

BASE_URL = "https://api.services.mimecast.com"


def get_most_used_contacts(token):
    """Fetches most-used contacts synced from Azure Active Directory."""
    print("Fetching most-used contacts...")
    api_url = f"{BASE_URL}/api/user/get-most-used-contacts"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    try:
        response = requests.post(api_url, headers=headers, json={})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching most-used contacts: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
        return None


if __name__ == "__main__":
    token = auth.get_token()
    resp = get_most_used_contacts(token)
    if not resp:
        raise SystemExit(1)

    contacts = []
    for block in resp.get("data", []) or []:
        if isinstance(block, dict) and "contacts" in block:
            contacts.extend(block["contacts"])

    print(f"\n--- Most-Used Contacts ({len(contacts)} total) ---")
    if contacts:
        print_records(contacts)
    else:
        print("No most-used contacts found.")

    fails = resp.get("fail", []) or []
    if fails:
        print("\n--- Failures ---")
        for f in fails:
            for err in f.get("errors", []):
                print(f"  {err.get('code')}: {err.get('message')}")
