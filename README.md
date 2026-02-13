# <img src="https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=700&size=35&pause=1000&color=1E90FF&width=800&height=50&lines=Mimecast+API+Toolkit+2.0" alt="Mimecast API Toolkit 2.0" />

> [!IMPORTANT]
> This project is an unofficial toolkit and is **not** affiliated with, maintained, or endorsed by Mimecast.

A collection of Python scripts to interact with the Mimecast API 2.0. This toolkit provides utilities for authentication, account management, email queue monitoring, threat intelligence, and more.

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

All scripts are in the `scripts/` directory. Run any script from the project root:
```bash
python3 scripts/<script_name>.py
```

Browse all available scripts:
```bash
ls scripts/*.py
```

> [!NOTE]
> Some scripts support interactive prompts, pagination, or command-line arguments. See [`docs/SCRIPT_REFERENCE.txt`](docs/SCRIPT_REFERENCE.txt) for details.

## Project Status

<p align="center">
  <img src="https://typograssy.deno.dev/api?text=Work%20in%20progress%20%20%20&l1=00ff2a&l2=22aa46&bg=000000&frame=5c5c5c&speed=100&comment=" alt="Work in progress" />
</p>
