import requests
import json
from datetime import datetime, timedelta, timezone
import auth

BASE_URL = "https://api.services.mimecast.com"

def get_audit_events(token, start_date=None, end_date=None, page_size=25, next_token=None):
    """Fetches a single page of Audit Events."""
    api_url = f"{BASE_URL}/api/audit/get-audit-events"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    now = datetime.now(timezone.utc)
    if not end_date:
        end_date = now
    if not start_date:
        start_date = end_date - timedelta(days=1)

    fmt = "%Y-%m-%dT%H:%M:%SZ"

    pagination = {"pageSize": page_size}
    if next_token:
        pagination["pageToken"] = next_token

    payload = {
        "meta": {
            "pagination": pagination
        },
        "data": [
            {
                "startDateTime": start_date.strftime(fmt),
                "endDateTime": end_date.strftime(fmt)
            }
        ]
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching audit events: {e}")
        if e.response is not None:
             print(f"Response: {e.response.text}")
        return None

def get_time_frame_choice():
    """Prompts user to select a time frame."""
    print("\nSelect a time frame:")
    print("1. Last hour")
    print("2. Last 24 hours")
    print("3. Last 7 days")
    print("4. Last 30 days")
    print("5. Last 60 days")
    print("6. Custom (specify start and end dates)")
    print("\nNote: API historical lookup is restricted to the last 60 days.")

    while True:
        choice = input("\nEnter your choice (1-6): ").strip()
        if choice in ['1', '2', '3', '4', '5', '6']:
            return choice
        print("Invalid choice. Please enter a number between 1 and 6.")

def get_custom_datetime(prompt_text):
    """Prompts user to enter a custom datetime."""
    while True:
        date_str = input(f"{prompt_text} (YYYY-MM-DD HH:MM or YYYY-MM-DD): ").strip()
        try:
            if ' ' in date_str:
                dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            else:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            print("Invalid format. Please use YYYY-MM-DD HH:MM or YYYY-MM-DD")

def get_page_size():
    """Prompts user to specify the number of results per page."""
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

if __name__ == "__main__":
    token = auth.get_token()

    # Get time frame
    choice = get_time_frame_choice()
    now = datetime.now(timezone.utc)

    if choice == '1':
        start_date = now - timedelta(hours=1)
        end_date = now
    elif choice == '2':
        start_date = now - timedelta(days=1)
        end_date = now
    elif choice == '3':
        start_date = now - timedelta(days=7)
        end_date = now
    elif choice == '4':
        start_date = now - timedelta(days=30)
        end_date = now
    elif choice == '5':
        start_date = now - timedelta(days=60)
        end_date = now
    else:  # choice == '6'
        print("\nEnter custom time frame:")
        start_date = get_custom_datetime("Start date/time")
        end_date = get_custom_datetime("End date/time")

    # Get page size
    page_size = get_page_size()

    # Display selected parameters
    print(f"\n{'='*50}")
    print(f"Time Frame: {start_date.strftime('%Y-%m-%d %H:%M:%S')} to {end_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Results per page: {page_size}")
    print(f"{'='*50}")

    all_events = []
    next_token = None
    page_num = 1

    while True:
        print(f"\nFetching page {page_num}...")
        events_data = get_audit_events(token, start_date, end_date, page_size, next_token)

        if not events_data:
            break

        data = events_data.get("data", [])
        all_events.extend(data)
        print(f"Got {len(data)} results (total so far: {len(all_events)})")

        meta = events_data.get("meta", {})
        pagination = meta.get("pagination", {})
        next_token = pagination.get("next")

        if not next_token:
            break

        fetch_more = input("\nMore results available. Fetch next page? (y/n, default y): ").strip().lower()
        if fetch_more == 'n':
            break
        page_num += 1

    print(f"\n--- Audit Events Results ({len(all_events)} total) ---")
    if not all_events:
        print("No audit events found for the selected period.")
    else:
        print(json.dumps(all_events, indent=2))