import requests
import auth
from table_utils import print_records
from get_internal_domains import get_internal_domains

BASE_URL = "https://api.services.mimecast.com"


def get_internal_users(token, domain, page_size=100, next_token=None):
    """Fetches a single page of internal users for a given domain."""
    api_url = f"{BASE_URL}/api/user/get-internal-users"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    pagination = {"pageSize": page_size}
    if next_token:
        pagination["pageToken"] = next_token

    payload = {
        "meta": {"pagination": pagination},
        "data": [{"domain": domain}],
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching internal users: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
        return None


def get_page_size():
    while True:
        try:
            size = input("\nHow many results per page? (1-100, default 100): ").strip()
            if not size:
                return 100
            size = int(size)
            if 1 <= size <= 100:
                return size
            print("Please enter a number between 1 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def choose_domain(token):
    """Fetch internal domains and let the user pick one."""
    resp = get_internal_domains(token)
    entries = []
    if resp:
        for block in resp.get("data", []) or []:
            if isinstance(block, dict) and "domains" in block:
                entries.extend(block["domains"])
            else:
                entries.append(block)

    names = []
    for d in entries:
        if isinstance(d, dict):
            name = d.get("domain") or d.get("name") or d.get("domainName")
            if name:
                names.append(name)
        elif isinstance(d, str):
            names.append(d)

    if not names:
        print("No internal domains parsed from response.")
        if resp:
            import json
            print("Raw response:")
            print(json.dumps(resp, indent=2)[:2000])
        return input("\nEnter internal domain manually: ").strip()

    print("\nInternal domains:")
    for i, name in enumerate(names, 1):
        print(f"  {i}. {name}")
    print(f"  {len(names) + 1}. Enter manually")

    while True:
        choice = input(f"\nSelect a domain (1-{len(names) + 1}): ").strip()
        try:
            idx = int(choice)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if 1 <= idx <= len(names):
            return names[idx - 1]
        if idx == len(names) + 1:
            return input("Enter internal domain: ").strip()
        print(f"Please enter a number between 1 and {len(names) + 1}.")


if __name__ == "__main__":
    token = auth.get_token()

    domain = choose_domain(token)
    if not domain:
        print("Domain is required.")
        raise SystemExit(1)

    page_size = get_page_size()

    print(f"\n{'='*50}")
    print(f"Domain: {domain}")
    print(f"Results per page: {page_size}")
    print(f"{'='*50}")

    total = 0
    next_token = None
    page_num = 1

    while True:
        print(f"\nFetching page {page_num}...")
        resp = get_internal_users(token, domain, page_size, next_token)
        if not resp:
            break

        page_users = []
        for block in resp.get("data", []) or []:
            if isinstance(block, dict) and "users" in block:
                page_users.extend(block["users"])
        total += len(page_users)
        print(f"Got {len(page_users)} results (total so far: {total})\n")

        if page_users:
            print_records(page_users)

        pagination = resp.get("meta", {}).get("pagination", {})
        next_token = pagination.get("next")
        if not next_token:
            break

        fetch_more = input("\nMore results available. Fetch next page? (y/n, default y): ").strip().lower()
        if fetch_more == 'n':
            break
        page_num += 1

    print(f"\n--- Internal Users for {domain} ({total} shown) ---")
    if total == 0:
        print("No users returned.")
