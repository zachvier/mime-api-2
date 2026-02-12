import requests
import auth

BASE_URL = "https://api.services.mimecast.com"

def get_hold_summary_list(token):
    """Fetches counts of currently held messages grouped by hold reason."""
    api_url = f"{BASE_URL}/api/gateway/get-hold-summary-list"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching hold summary: {e}")
        if e.response is not None:
             print(f"Response: {e.response.text}")
        return None

if __name__ == "__main__":
    token = auth.get_token()

    print("\nFetching held message summary...")
    summary_data = get_hold_summary_list(token)

    if not summary_data:
        print("Failed to fetch hold summary.")
    else:
        data = summary_data.get("data", [])
        print(f"\n--- Hold Summary ({len(data)} reasons) ---")
        if not data:
            print("No held messages found.")
        else:
            total = 0
            for item in data:
                count = item.get("numberOfItems", 0)
                policy = item.get("policyInfo", "Unknown")
                total += count
                print(f"  {policy}: {count}")
            print(f"\n  Total held: {total}")
