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

This toolkit includes scripts organized by functional area:

**Account & Identity**
- Account information, emergency contacts, support info, identity verification

**Security & Threat Protection**
- URL decoding, TTP logs (attachment, impersonation), managed URLs

**Gateway & Message Management**
- Email queues, held/release logs, hold message lists and summaries

**Auditing & Compliance**
- Audit events, audit categories, archive search logs, provisioning packages

**Monitoring**
- Dashboard notifications, message tracking

For a complete list of available scripts, browse the `scripts/` directory:
```bash
ls scripts/*.py
```

### Advanced Usage

**Interactive Scripts with Pagination**

Several scripts offer interactive time frame selection and automatic pagination:

- **`get_audit_events.py`** - Audit event retrieval with filtering
- **`get_held_release_logs.py`** - Held/release message logs
- **`get_hold_message_list.py`** - Held messages with admin filtering

These scripts prompt you to:
1. Select time frame (last hour, 24h, 7 days, 30 days, or custom dates)
2. Choose results per page (1-500, default 100)
3. Optionally fetch additional pages when more results are available

Example:
```bash
python3 scripts/get_audit_events.py
# Follow the interactive prompts
```

**URL Decoder**

The `decode_url.py` script can be used interactively or with command-line arguments:

*   **Argument Mode:**
    ```bash
    python3 scripts/decode_url.py "https://url.us.m.mimecastprotect.com/..."
    ```

*   **Interactive Mode:**
    ```bash
    python3 scripts/decode_url.py
    # Follow the prompt to paste the URL
    ```

## Project Status

<p align="center">
  <img src="https://typograssy.deno.dev/api?text=Work%20in%20progress%20%20%20&l1=00ff2a&l2=22aa46&bg=000000&frame=5c5c5c&speed=100&comment=" alt="Work in progress" />
</p>
