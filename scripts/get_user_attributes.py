import base64
import os
import re
import requests
import auth
from table_utils import print_records

BASE_URL = "https://api.services.mimecast.com"


def get_user_attributes(token, email_address):
    api_url = f"{BASE_URL}/api/user/get-attributes"
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
        print(f"Error fetching attributes: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
        return None


if __name__ == "__main__":
    token = auth.get_token()

    email = input("\nEnter email address: ").strip()
    if not email:
        print("Email address is required.")
        raise SystemExit(1)

    print(f"\n{'='*50}")
    print(f"Email: {email}")
    print(f"{'='*50}\n")

    resp = get_user_attributes(token, email)
    if not resp:
        raise SystemExit(1)

    attributes = []
    for block in resp.get("data", []) or []:
        if isinstance(block, dict) and "attributes" in block:
            attributes.extend(block["attributes"])

    print(f"--- Attributes for {email} ({len(attributes)} total) ---")
    if attributes:
        print_records(attributes)
    else:
        print("No attributes found.")

    photos = [a for a in attributes if a.get("name") == "thumbnailPhoto" and a.get("value")]
    for i, photo in enumerate(photos, 1):
        label = f" ({i}/{len(photos)})" if len(photos) > 1 else ""
        choice = input(f"\nthumbnailPhoto found{label}. Save to current directory? [Y/n]: ").strip().lower()
        if choice in ("", "y", "yes"):
            safe = re.sub(r"[^A-Za-z0-9._-]", "_", email)
            suffix = f"_{i}" if len(photos) > 1 else ""
            filename = f"{safe}{suffix}_thumbnail.jpg"
            path = os.path.join(os.getcwd(), filename)
            try:
                with open(path, "wb") as f:
                    f.write(base64.b64decode(photo["value"]))
                print(f"Saved: {path}")
            except (base64.binascii.Error, OSError) as e:
                print(f"Could not save image: {e}")

    fails = resp.get("fail", []) or []
    if fails:
        print("\n--- Failures ---")
        for f in fails:
            for err in f.get("errors", []):
                print(f"  {err.get('code')}: {err.get('message')}")
