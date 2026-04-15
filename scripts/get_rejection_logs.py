import requests
import json
from datetime import datetime, timedelta, timezone
import auth
from table_utils import print_records

BASE_URL = "https://api.services.mimecast.com"

def get_rejections(token, start_date, end_date, page_size=100, next_token=None):
    """Fetches a single page of gateway rejection logs."""
    api_url = f"{BASE_URL}/api/gateway/get-rejections"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    fmt = "%Y-%m-%dT%H:%M:%SZ"
    pagination = {"pageSize": page_size}
    if next_token:
        pagination["pageToken"] = next_token

    payload = {
        "meta": {"pagination": pagination},
        "data": [
            {
                "admin": True,
                "start": start_date.strftime(fmt),
                "end": end_date.strftime(fmt)
            }
        ]
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching rejections: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
        return None

def get_time_frame_choice():
    print("\nSelect a time frame:")
    print("1. Last hour")
    print("2. Last 24 hours")
    print("3. Last 7 days")
    print("4. Last 30 days")
    print("5. Custom")
    while True:
        choice = input("\nEnter your choice (1-5): ").strip()
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        print("Invalid choice.")

def get_custom_datetime(prompt_text):
    while True:
        date_str = input(f"{prompt_text} (YYYY-MM-DD HH:MM or YYYY-MM-DD): ").strip()
        try:
            if ' ' in date_str:
                dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            else:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            print("Invalid format.")

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
            print("Invalid input.")

if __name__ == "__main__":
    token = auth.get_token()
    choice = get_time_frame_choice()
    now = datetime.now(timezone.utc)

    if choice == '1':
        start_date, end_date = now - timedelta(hours=1), now
    elif choice == '2':
        start_date, end_date = now - timedelta(days=1), now
    elif choice == '3':
        start_date, end_date = now - timedelta(days=7), now
    elif choice == '4':
        start_date, end_date = now - timedelta(days=30), now
    else:
        print("\nEnter custom time frame:")
        start_date = get_custom_datetime("Start date/time")
        end_date = get_custom_datetime("End date/time")

    page_size = get_page_size()

    print(f"\n{'='*50}")
    print(f"Time Frame: {start_date.strftime('%Y-%m-%d %H:%M:%S')} to {end_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Results per page: {page_size}")
    print(f"{'='*50}")

    all_events = []
    next_token = None
    page_num = 1

    while True:
        print(f"\nFetching page {page_num}...")
        data_resp = get_rejections(token, start_date, end_date, page_size, next_token)
        if not data_resp:
            break

        page_rows = []
        for block in data_resp.get("data", []):
            page_rows.extend(block.get("rejections", []))
        all_events.extend(page_rows)
        print(f"Got {len(page_rows)} results (total so far: {len(all_events)})")

        next_token = data_resp.get("meta", {}).get("pagination", {}).get("next")
        if not next_token:
            break

        fetch_more = input("\nMore results available. Fetch next page? (y/n, default y): ").strip().lower()
        if fetch_more == 'n':
            break
        page_num += 1

    print(f"\n--- Rejection Logs ({len(all_events)} total) ---")
    if not all_events:
        print("No rejections found for the selected period.")
    else:
        print_records(all_events)
