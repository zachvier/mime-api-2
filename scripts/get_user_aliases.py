import requests
import auth
from table_utils import print_records

BASE_URL = "https://api.services.mimecast.com"


def get_user_aliases(token, email_address):
    api_url = f"{BASE_URL}/api/user/get-aliases"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {"data": [{"emailAddress": email_address}]}

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching aliases: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
        return None


if __name__ == "__main__":
    token = auth.get_token()

    email = input("\nEnter primary email address: ").strip()
    if not email:
        print("Email address is required.")
        raise SystemExit(1)

    print(f"\n{'='*50}")
    print(f"Email: {email}")
    print(f"{'='*50}\n")

    resp = get_user_aliases(token, email)
    if not resp:
        raise SystemExit(1)

    aliases = []
    for block in resp.get("data", []) or []:
        if isinstance(block, dict) and "aliases" in block:
            aliases.extend(block["aliases"])

    print(f"--- Aliases for {email} ({len(aliases)} total) ---")
    if aliases:
        print_records(aliases)
    else:
        print("No aliases found.")

    fails = resp.get("fail", []) or []
    if fails:
        print("\n--- Failures ---")
        for f in fails:
            for err in f.get("errors", []):
                print(f"  {err.get('code')}: {err.get('message')}")
