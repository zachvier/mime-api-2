# <img src="https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=700&size=35&pause=1000&color=1E90FF&width=800&height=50&lines=Mimecast+API+Toolkit+2.0" alt="Mimecast API Toolkit 2.0" />

> [!IMPORTANT]
> This project is an unofficial toolkit and is **not** affiliated with, maintained, or endorsed by Mimecast.

A collection of Python scripts to interact with the Mimecast API 2.0. This toolkit provides utilities for authentication, account management, email queue monitoring, threat intelligence, and more.

## Features

- **Centralized Authentication:** OAuth2 token management handled automatically.
- **Account Insights:** Retrieve detailed account info, support details, and emergency contacts.
- **Monitoring:** Check email queues and dashboard notifications.
- **Security:** Decode rewritten URLs, fetch archive search logs, and list managed URLs.
- **Auditing:** Retrieve audit event categories.
- **Provisioning:** View account packages.
- **Identity:** Verify partner and account identity information.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/zachvier/mimecast-api-2.0.git
    cd mimecast-api-2.0
    ```

2.  **Install dependencies:**
    ```bash
    pip3 install -r requirements.txt
    ```

3.  **Configure Credentials:**
    Create a `credentials.txt` file in the `scripts/` directory (or root, depending on where you run from) with your Mimecast API Client ID and Secret:
    ```text
    client_id=YOUR_CLIENT_ID
    client_secret=YOUR_CLIENT_SECRET
    ```
    *Note: `credentials.txt` is git-ignored for security.*

    **Finding your Account Code:**
    Once configured, run the account script to find your `account_code`:
    ```bash
    python3 scripts/get_account.py
    ```
    Then, add it to your `credentials.txt`:
    ```text
    client_id=YOUR_CLIENT_ID
    client_secret=YOUR_CLIENT_SECRET
    account_code=YOUR_ACCOUNT_CODE
    ```

## Usage

All scripts are located in the `scripts/` directory. You can run them from the project root using:

```bash
python3 scripts/<script_name>.py
```

### Available Scripts

| Script Name | Description |
| :--- | :--- |
| `get_account.py` | Retrieves detailed account information. |
| `get_dashboard_notifications.py` | Fetches dashboard notifications for the configured account. |
| `get_email_queues.py` | Monitors inbound and outbound email queues for the last 24 hours. |
| `get_emergency_contact.py` | Retrieves account emergency contact details. |
| `get_support_info.py` | Fetches support information for your Mimecast account. |
| `get_archive_search_logs.py` | Retrieves archive search logs (supports pagination). |
| `get_whoami.py` | Fetches identity information (whoami). |
| `decode_url.py` | Decodes Mimecast rewritten URLs (TTP). |
| `get_audit_categories.py` | Retrieves audit event categories. |
| `get_audit_events.py` | Interactive audit event retrieval with time frame selection and pagination. |
| `get_provisioning_packages.py` | Retrieves provisioning packages for the account. |
| `get_all_managed_urls.py` | Fetches all TTP managed URLs. |
| `get_ttp_attachment_logs.py` | Fetches TTP attachment protection logs (last 7 days). |
| `get_ttp_impersonation_logs.py` | Fetches TTP impersonation protection logs (last 7 days). |

### Advanced Usage

**URL Decode (`decode_url.py`)**

This script can be used interactively or with command-line arguments.

*   **Argument Mode:**
    ```bash
    python3 scripts/decode_url.py "https://url.us.m.mimecastprotect.com/..."
    ```

*   **Interactive Mode:**
    ```bash
    python3 scripts/decode_url.py
    # Follow the prompt to paste the URL
    ```

**Audit Events (`get_audit_events.py`)**

This script prompts you to select a time frame and page size, then automatically handles pagination:

```bash
python3 scripts/get_audit_events.py
# 1. Select time frame (last hour, 24h, 7 days, 30 days, or custom)
# 2. Choose results per page (up to 500)
# 3. Optionally fetch additional pages when more results are available
```

## Project Status

<p align="center">
  <img src="https://typograssy.deno.dev/api?text=Work%20in%20progress%20%20%20&l1=00ff2a&l2=22aa46&bg=000000&frame=5c5c5c&speed=100&comment=" alt="Work in progress" />
</p>
