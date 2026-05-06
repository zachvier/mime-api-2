#!/usr/bin/env python3
import getpass
import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import auth
from registry import SCRIPT_REGISTRY, script_lookup


CREDENTIAL_ENV_KEYS = (
    "MIMECAST_CLIENT_ID",
    "CLIENT_ID",
    "MIMECAST_CLIENT_SECRET",
    "CLIENT_SECRET",
)
ACCOUNT_CODE_ENV_KEYS = ("MIMECAST_ACCOUNT_CODE", "ACCOUNT_CODE")
AREA_LABELS = {
    "Account & Identity": "account",
    "Gateway - Logs With Time Frames": "gateway logs",
    "Gateway - Other": "gateway",
    "DLP & TTP Logs": "dlp/ttp",
    "Directory & Domains": "directory",
    "URLs & Archive": "urls/archive",
    "URL Decoder": "decoder",
}


def is_placeholder(value):
    return not value or "YOUR_" in value


def has_usable_credentials(config):
    return not is_placeholder(config.get("client_id")) and not is_placeholder(
        config.get("client_secret")
    )


def status_label(value):
    if not value:
        return "missing"
    if "YOUR_" in value:
        return "placeholder"
    return "found"


def print_credential_status(config):
    print("Credential status:")
    print(f"  client_id     : {status_label(config.get('client_id'))}")
    print(f"  client_secret : {status_label(config.get('client_secret'))}")
    print(f"  account_code  : {status_label(config.get('account_code'))}")


def prompt_inline_credentials(existing_config):
    print("\nNo usable stored client credentials found.")
    print("Enter credentials for this session only. They will not be saved.")

    client_id = input("Mimecast client ID: ").strip()
    client_secret = getpass.getpass("Mimecast client secret: ").strip()
    account_code = input("Account code (optional): ").strip()

    overrides = {
        "client_id": client_id,
        "client_secret": client_secret,
    }
    if account_code:
        overrides["account_code"] = account_code
    elif existing_config.get("account_code"):
        overrides["account_code"] = existing_config["account_code"]

    return overrides


def authenticate():
    config = auth.get_config()
    print_credential_status(config)

    overrides = None
    if not has_usable_credentials(config):
        overrides = prompt_inline_credentials(config)
        config = auth.get_config(overrides)

    token = auth.get_token(overrides)
    if not token:
        print("Authentication succeeded, but no access token was returned.")
        return None, config

    print("Authentication ready.")
    return token, config


def format_note(entry):
    notes = []
    if entry.requires_account_code:
        notes.append("requires account_code")
    if entry.notes:
        notes.append(entry.notes)
    return f" ({'; '.join(notes)})" if notes else ""


def area_label(entry):
    return AREA_LABELS.get(entry.category, entry.category.lower())


def print_script_table(entries=SCRIPT_REGISTRY, interactive=True):
    print("\nMimecast API Toolkit")
    print("====================")
    print(f"{'Script':<30} {'Area':<14} {'Title':<28} Need")
    print("-" * 82)
    for entry in entries:
        need = "account_code" if entry.requires_account_code else ""
        print(f"{entry.command_name:<30} {area_label(entry):<14} {entry.title:<28} {need}")

    if interactive:
        print("\nEnter a script name to view/run it, text to search, r to reset, or q to quit.")


def find_script(name):
    normalized = name.strip()
    if not normalized:
        return None
    lookup = script_lookup()
    if normalized in lookup:
        return lookup[normalized]
    if not normalized.endswith(".py") and f"{normalized}.py" in lookup:
        return lookup[f"{normalized}.py"]
    return None


def search_entries(query):
    needle = query.strip().lower()
    if not needle:
        return tuple(SCRIPT_REGISTRY)

    matches = []
    for entry in SCRIPT_REGISTRY:
        haystack = " ".join(
            [
                entry.filename,
                entry.command_name,
                entry.category,
                entry.title,
                entry.description,
                entry.notes,
            ]
        ).lower()
        if needle in haystack:
            matches.append(entry)
    return tuple(matches)


def print_script_detail(entry):
    print("\nScript")
    print("------")
    print(f"Name        : {entry.command_name}")
    print(f"File        : scripts/{entry.filename}")
    print(f"Area        : {entry.category}")
    print(f"Description : {entry.description}")
    if entry.requires_account_code:
        print("Requires    : account_code")
    if entry.notes:
        print(f"Notes       : {entry.notes}")


def confirm_and_run(entry, token, config):
    print_script_detail(entry)
    choice = input("\nPress Enter to run, b to go back, or q to quit: ").strip().lower()
    if choice == "q":
        return "quit"
    if choice == "b":
        return "back"
    run_entry(entry, token, config)
    input("\nPress Enter to return to the script table...")
    return "back"


def build_child_env(token, account_code=None, base_env=None):
    env = dict(base_env if base_env is not None else os.environ)
    for key in CREDENTIAL_ENV_KEYS:
        env.pop(key, None)
    env["MIMECAST_ACCESS_TOKEN"] = token
    env.pop("ACCESS_TOKEN", None)

    for key in ACCOUNT_CODE_ENV_KEYS:
        env.pop(key, None)
    if account_code:
        env["MIMECAST_ACCOUNT_CODE"] = account_code

    return env


def run_entry(entry, token, config):
    script_path = SCRIPTS_DIR / entry.filename
    if not script_path.exists():
        print(f"Script not found: {script_path}")
        return 1

    if entry.requires_account_code and not config.get("account_code"):
        print("Warning: this script requires account_code and none is configured.")

    env = build_child_env(token, config.get("account_code"))
    command = [sys.executable, str(script_path)]
    print(f"\nRunning {entry.filename}...\n")
    completed = subprocess.run(command, cwd=str(PROJECT_ROOT), env=env)
    print(f"\n{entry.filename} exited with status {completed.returncode}.")
    return completed.returncode


def run_interactive(token, config):
    current_entries = SCRIPT_REGISTRY
    while True:
        print_script_table(current_entries)
        choice = input("\nScript name: ").strip()

        if choice.lower() == "q":
            return 0
        if choice.lower() == "r":
            current_entries = SCRIPT_REGISTRY
            continue

        entry = find_script(choice)
        if entry:
            result = confirm_and_run(entry, token, config)
            if result == "quit":
                return 0
            current_entries = SCRIPT_REGISTRY
            continue

        matches = search_entries(choice)
        if not matches:
            print(f"No scripts matched: {choice}")
            continue
        current_entries = matches


def list_scripts():
    print_script_table(SCRIPT_REGISTRY, interactive=False)
    return 0


def run_named_script(name):
    entry = find_script(name)
    if not entry:
        print(f"Unknown script: {name}")
        return 2

    token, config = authenticate()
    if not token:
        return 1
    return run_entry(entry, token, config)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)

    if argv and argv[0] in {"-h", "--help", "help"}:
        print("Usage:")
        print("  python3 mimecast_toolkit.py")
        print("  python3 mimecast_toolkit.py list")
        print("  python3 mimecast_toolkit.py run <script_name>")
        return 0

    if argv and argv[0] == "list":
        return list_scripts()

    if argv and argv[0] == "run":
        if len(argv) < 2:
            print("Usage: python3 mimecast_toolkit.py run <script_name>")
            return 2
        return run_named_script(argv[1])

    if argv:
        print(f"Unknown command: {' '.join(argv)}")
        return 2

    token, config = authenticate()
    if not token:
        return 1
    return run_interactive(token, config)


if __name__ == "__main__":
    sys.exit(main())
