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
CONFIG_ALIASES = {
    "mimecast_client_id": "client_id",
    "mimecast_client_secret": "client_secret",
    "mimecast_account_code": "account_code",
}
TOKEN_ENV_KEYS = ("MIMECAST_ACCESS_TOKEN", "ACCESS_TOKEN")

def get_credentials(config_overrides=None):
    """Reads client_id and client_secret from a text file."""
    creds = get_config(config_overrides)
    return creds.get("client_id"), creds.get("client_secret")

def get_config(config_overrides=None):
    """Reads config from environment variables, .env, credentials.txt, and overrides."""
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
                    key = key.strip().lower()
                    key = CONFIG_ALIASES.get(key, key)
                    creds[key] = value.strip()
    except FileNotFoundError:
        pass

    if config_overrides:
        for key, value in config_overrides.items():
            normalized_key = CONFIG_ALIASES.get(str(key).strip().lower(), str(key).strip().lower())
            if normalized_key in CONFIG_KEYS and value:
                creds[normalized_key] = str(value).strip()
    return creds

def get_token(config_overrides=None):
    """Obtains the Bearer token, or reuses one supplied by the launcher."""
    for env_key in TOKEN_ENV_KEYS:
        access_token = os.getenv(env_key)
        if access_token:
            return access_token.strip()

    client_id, client_secret = get_credentials(config_overrides)
    
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
