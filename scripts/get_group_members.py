import requests
import auth
from table_utils import print_records

BASE_URL = "https://api.services.mimecast.com"


def get_group_members(token, group_id):
    """Fetches members for a directory group."""
    api_url = f"{BASE_URL}/api/directory/get-group-members"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {"data": [{"id": group_id}]}

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching group members: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
        return None


def maybe_show_groups(token):
    choice = input("\nList groups first? (y/n, default n): ").strip().lower()
    if choice not in ("y", "yes"):
        return

    try:
        from find_groups import find_groups, pick_source
    except ImportError as e:
        print(f"Could not load find_groups helper: {e}")
        return

    source = pick_source()
    query = input("\nOptional group search query (blank for all): ").strip() or None
    resp = find_groups(token, query=query, source=source)
    if not resp:
        return

    groups = []
    for block in resp.get("data", []) or []:
        if isinstance(block, dict) and "folders" in block:
            groups.extend(block["folders"])

    print(f"\n--- Matching Groups ({len(groups)} shown) ---")
    if groups:
        print_records(groups)
    else:
        print("No groups found.")


if __name__ == "__main__":
    token = auth.get_token()

    maybe_show_groups(token)
    group_id = input("\nEnter group ID: ").strip()
    if not group_id:
        print("Group ID is required.")
        raise SystemExit(1)

    print(f"\n{'='*50}")
    print(f"Group ID: {group_id}")
    print(f"{'='*50}\n")

    resp = get_group_members(token, group_id)
    if not resp:
        raise SystemExit(1)

    members = []
    for block in resp.get("data", []) or []:
        if isinstance(block, dict) and "groupMembers" in block:
            members.extend(block["groupMembers"])

    print(f"--- Group Members ({len(members)} total) ---")
    if members:
        print_records(members)
    else:
        print("No group members found.")

    fails = resp.get("fail", []) or []
    if fails:
        print("\n--- Failures ---")
        for f in fails:
            for err in f.get("errors", []):
                print(f"  {err.get('code')}: {err.get('message')}")
