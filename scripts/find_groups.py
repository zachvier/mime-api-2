import requests
import json
import auth
from table_utils import print_records

BASE_URL = "https://api.services.mimecast.com"

SOURCES = ["cloud", "ldap"]

def find_groups(token, query=None, source="cloud", page_size=100, next_token=None):
    """Fetches a single page of directory groups."""
    api_url = f"{BASE_URL}/api/directory/find-groups"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    pagination = {"pageSize": page_size}
    if next_token:
        pagination["pageToken"] = next_token

    entry = {"source": source}
    if query:
        entry["query"] = query

    payload = {
        "meta": {"pagination": pagination},
        "data": [entry]
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error finding groups: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
        return None

def pick_source():
    print("\nSelect group source:")
    for i, s in enumerate(SOURCES, 1):
        marker = " (default)" if s == "cloud" else ""
        print(f"{i}. {s}{marker}")
    while True:
        choice = input(f"Choose 1-{len(SOURCES)} (default 1): ").strip()
        if not choice:
            return "cloud"
        if choice.isdigit() and 1 <= int(choice) <= len(SOURCES):
            return SOURCES[int(choice) - 1]
        print("Invalid choice.")

if __name__ == "__main__":
    token = auth.get_token()

    source = pick_source()
    query = input("\nOptional search query (blank for all): ").strip() or None

    all_groups = []
    next_token = None
    page_num = 1

    while True:
        print(f"\nFetching page {page_num}...")
        resp = find_groups(token, query=query, source=source, next_token=next_token)
        if not resp:
            break

        page_groups = []
        for block in resp.get("data", []):
            page_groups.extend(block.get("folders", []))
        all_groups.extend(page_groups)
        print(f"Got {len(page_groups)} groups (total so far: {len(all_groups)})")

        next_token = resp.get("meta", {}).get("pagination", {}).get("next")
        if not next_token:
            break

        fetch_more = input("\nMore results available. Fetch next page? (y/n, default y): ").strip().lower()
        if fetch_more == 'n':
            break
        page_num += 1

    print(f"\n--- Directory Groups ({len(all_groups)} total) ---")
    if not all_groups:
        print("No groups found.")
    else:
        print_records(all_groups)
