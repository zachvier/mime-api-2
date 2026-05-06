# <img src="https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=700&size=35&pause=1000&color=1E90FF&width=800&height=50&lines=Mimecast+API+Toolkit+2.0" alt="Mimecast API Toolkit 2.0" />

> [!IMPORTANT]
> This project is an unofficial toolkit and is **not** affiliated with, maintained, or endorsed by Mimecast.

A collection of Python scripts for the Mimecast API 2.0. Covers account info, gateway logs, held/released messages, DLP, TTP (URL/attachment/impersonation) logs, directory groups and members, delegates, most-used contacts, managed URLs, and more.

## Installation

1. **Clone:**
   ```bash
   git clone https://github.com/zachvier/mime-api-2.git
   cd mime-api-2
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Configure credentials:**
   Create `scripts/credentials.txt`:
   ```text
   client_id=YOUR_CLIENT_ID
   client_secret=YOUR_CLIENT_SECRET
   ```
   *`credentials.txt` is git-ignored.*

   You can also use a project-root `.env` file or exported environment variables:
   ```text
   MIMECAST_CLIENT_ID=YOUR_CLIENT_ID
   MIMECAST_CLIENT_SECRET=YOUR_CLIENT_SECRET
   MIMECAST_ACCOUNT_CODE=YOUR_ACCOUNT_CODE
   ```

   **Find your account code** (needed for a couple of scripts):
   ```bash
   python3 scripts/get_account.py
   ```
   Then add it:
   ```text
   account_code=YOUR_ACCOUNT_CODE
   ```

## Usage

Start the terminal launcher from the project root:
```bash
python3 mimecast_toolkit.py
```

The launcher checks credentials, authenticates once, then shows a compact script
table. Enter a script name to open its detail page and run it. If no stored
credentials are found, it prompts for session-only credentials and does not save
them.


```
Credential status:
  client_id     : found
  client_secret : found
  account_code  : found
Authenticating...
Authentication ready.

Mimecast API Toolkit
====================
Script                         Area           Title                        Need
----------------------------------------------------------------------------------
get_account                    account        Account info
get_support_info               account        Support info
get_emergency_contact          account        Emergency contact
get_whoami                     account        Whoami
get_dashboard_notifications    account        Dashboard notifications      account_code
get_rejection_logs             gateway logs   Rejection logs
get_held_release_logs          gateway logs   Held/release logs
get_hold_message_list          gateway logs   Held message list
get_audit_events               gateway logs   Audit events
get_hold_summary_list          gateway        Hold summary
get_email_queues               gateway        Email queues
get_gateway_details            gateway        Gateway details
get_outbound_ip_addresses      gateway        Outbound IP addresses
get_email_statistics           gateway        Email statistics
get_dlp_logs                   dlp/ttp        DLP logs
get_ttp_url_logs               dlp/ttp        TTP URL logs
get_ttp_attachment_logs        dlp/ttp        TTP attachment logs
get_ttp_impersonation_logs     dlp/ttp        TTP impersonation logs
find_groups                    directory      Find groups
get_group_members              directory      Group members
get_internal_domains           directory      Internal domains
get_internal_users             directory      Internal users
get_directory_connections      directory      Directory connections
get_user_aliases               directory      User aliases
get_user_attributes            directory      User attributes
find_delegate_users            directory      Delegate users
get_most_used_contacts         directory      Most-used contacts
get_all_managed_urls           urls/archive   Managed URLs
get_archive_search_logs        urls/archive   Archive search logs
get_audit_categories           urls/archive   Audit categories
get_provisioning_packages      urls/archive   Provisioning packages
decode_url                     decoder        Decode URL

Enter a script name to view/run it, text to search, r to reset, or q to quit.
```

List scripts without authenticating:
```bash
python3 mimecast_toolkit.py list
```

Run a specific script through the launcher:
```bash
python3 mimecast_toolkit.py run get_account
```

You can still run any script directly from the project root:
```bash
python3 scripts/<script_name>.py
```

## Output format

All record-producing scripts share a consistent vertical format via the shared `table_utils.print_records` helper — each record is printed as a labeled `key : value` block with aligned key widths. Nested values are rendered as compact JSON. This keeps heterogeneous API responses readable without column truncation.

A handful of scripts intentionally use custom output for non-record shapes (`decode_url`, `get_email_queues`, `get_hold_summary_list`).

## Script reference

See [`docs/SCRIPT_REFERENCE.txt`](docs/SCRIPT_REFERENCE.txt) for the full list — grouped by category, with interactive prompts and arguments called out.

## Project Status

<p align="center">
  <img src="https://typograssy.deno.dev/api?text=Work%20in%20progress%20%20%20&l1=00ff2a&l2=22aa46&bg=000000&frame=5c5c5c&speed=100&comment=" alt="Work in progress" />
</p>
