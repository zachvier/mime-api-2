import requests
import sys
import os
from dotenv import load_dotenv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
CREDENTIALS_FILE = os.path.join(SCRIPT_DIR, "credentials.txt")
ENV_FILE = os.path.join(PROJECT_ROOT, ".env")
BASE_URL = "https://api.services.mimecast.com"
CONFIG_KEYS = ("client_id", "client_secret", "account_code")

def get_credentials():
    """Reads client_id and client_secret from a text file."""
    creds = get_config()
    return creds.get("client_id"), creds.get("client_secret")

def get_config():
    """Reads config from environment variables, .env, and credentials.txt."""
    load_dotenv(ENV_FILE)

    creds = {}
    for key in CONFIG_KEYS:
        env_key = key.upper()
        prefixed_env_key = f"MIMECAST_{env_key}"
        value = os.getenv(prefixed_env_key) or os.getenv(env_key)
        if value:
            creds[key] = value.strip()

    try:
        with open(CREDENTIALS_FILE, "r") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    creds[key.strip().lower()] = value.strip()
    except FileNotFoundError:
        pass
    return creds

def get_token():
    """Obtains the Bearer token using credentials from file."""
    client_id, client_secret = get_credentials()
    
    if (
        not client_id
        or not client_secret
        or "YOUR_" in client_id
        or "YOUR_" in client_secret
    ):
        print(f"Please set API credentials in {CREDENTIALS_FILE}, .env, or environment variables.")
        sys.exit(1)

    print("Authenticating...")
    url = f"{BASE_URL}/oauth/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    try:
        response = requests.post(url, data=payload, timeout=30)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"Error obtaining token: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
        sys.exit(1)
