import requests
import json
import auth
import sys
from datetime import datetime, timedelta, timezone
from table_utils import print_records

BASE_URL = "https://api.services.mimecast.com"

def get_notifications(token, account_code):
    """Fetches Dashboard Notifications for the specified account."""
    print("Fetching Dashboard Notifications...")
    api_url = f"{BASE_URL}/api/account/get-dashboard-notifications"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "data": [
            {
                "accountCode": account_code
            }
        ]
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching notifications: {e}")
        if e.response is not None:
             print(f"Response: {e.response.text}")
        return None

def filter_recent_notifications(data, years=2):
    """Filters notifications to keep only those from the last 'years'."""
    if not data or not isinstance(data, list):
        return data

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=years * 365)
    
    # The date format is like "2026-01-23T18:19:13+0000"
    # %z matches +0000
    date_fmt = "%Y-%m-%dT%H:%M:%S%z"

    for item in data:
        if "notifications" in item:
            filtered_notifs = []
            for notif in item["notifications"]:
                visible_from_str = notif.get("visibleFrom")
                if visible_from_str:
                    try:
                        # Parse the date
                        visible_from = datetime.strptime(visible_from_str, date_fmt)
                        if visible_from >= cutoff_date:
                            filtered_notifs.append(notif)
                    except ValueError:
                        # If date parsing fails, keep it to be safe or maybe log? 
                        # We'll keep it to avoid hiding potentially important malformed items.
                        filtered_notifs.append(notif)
            item["notifications"] = filtered_notifs
            
    return data

if __name__ == "__main__":
    token = auth.get_token()
    config = auth.get_config()
    account_code = config.get("account_code")
    
    if not account_code:
        print("Error: 'account_code' not found in credentials.txt")
        print("Please add 'account_code=YOUR_ACCOUNT_CODE' to credentials.txt")
        sys.exit(1)

    notifications_data = get_notifications(token, account_code)
    
    if notifications_data:
        print("\n--- Dashboard Notifications (Last 2 Years) ---")
        data = notifications_data.get("data", [])
        
        # Filter the data
        data = filter_recent_notifications(data)

        rows = []
        for block in data:
            rows.extend(block.get("notifications", []))

        if not rows:
            print("No notifications found.")
        else:
            print(f"({len(rows)} notifications)")
            print_records(rows)
