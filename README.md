# <img src="https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=700&size=35&pause=1000&color=1E90FF&width=800&height=50&lines=Mimecast+API+Toolkit+2.0" alt="Mimecast API Toolkit 2.0" />

> [!IMPORTANT]
> This project is an unofficial toolkit and is **not** affiliated with, maintained, or endorsed by Mimecast.

A collection of Python scripts for the Mimecast API 2.0. Covers account info, gateway logs, held/released messages, DLP, TTP (URL/attachment/impersonation) logs, directory groups, managed URLs, and more.

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

Run any script from the project root:
```bash
python3 scripts/<script_name>.py
```

List all available scripts:
```bash
ls scripts/*.py
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
