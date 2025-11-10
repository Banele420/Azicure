# Azicure v0.4 — Trust Infrastructure ++

Azicure is a reference implementation of a zero-trust content pipeline. It packages
cryptographic primitives, device whitelisting, and time-based one-time password
(TOTP) verification behind a simple command-line interface (CLI) and a FastAPI
service so teams can bootstrap secure document workflows quickly.

## Features

- **Master-key–derived file encryption** using AES-GCM with per-file data keys.
- **Device allow list** tracked on disk to gate access to encryption endpoints.
- **TOTP enrollment and verification** for second-factor protection of API calls.
- **Tamper manifest tooling** to detect unauthorized file modifications.
- **FastAPI service** that wraps the crypto primitives behind REST endpoints.

## Repository layout

```
azicure_dynamic_versioning/azicure
├── configs/               # Default locations for keys, allow list, and manifests
├── data/                  # Sample data files for local testing
├── docker/                # Container helpers (not required for local usage)
├── docs/                  # Architecture, release, and onboarding guides
├── src/azicure/           # Python package with CLI, API, and core modules
├── tests/                 # Smoke tests for packaging/import validation
└── README.md              # This guide
```

## Prerequisites

- Python 3.9 or newer
- `pip` and `virtualenv`/`venv`
- An authenticator application that can scan TOTP provisioning URIs (e.g.,
  Google Authenticator, 1Password, Authy)

## Installation

1. **Clone the repository and unzip the source bundle if applicable.**
   ```bash
   git clone <repo-url>
   cd Azicure/azicure_dynamic_versioning/azicure
   ```
2. **Create and activate a virtual environment.**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. **Install Azicure and its dependencies.**
   ```bash
   pip install -e .
   ```
   For development tooling (tests, linting, packaging helpers) install the
   optional extras:
   ```bash
   pip install -e .[dev]
   ```

## Configuration

Azicure reads runtime configuration from environment variables (optionally
provided by a `.env` file loaded through `python-dotenv`). Defaults are shown
below:

| Variable | Default | Purpose |
| --- | --- | --- |
| `AZICURE_MASTER_KEY_FILE` | `./configs/master_key.bin` | Location of the symmetric master key used to wrap file data keys. |
| `AZICURE_DEVICE_REGISTRY` | `./configs/device_registry.json` | Path to the JSON whitelist of approved device IDs. |
| `AZICURE_LOG_DIR` | `./logs` | Directory where structured logs are written. |
| `AZICURE_TAMPER_MANIFEST` | `./configs/tamper_manifest.json` | Manifest file that records checksums for tamper detection. |
| `AZICURE_ISSUER` | `Azicure` | Issuer label embedded in TOTP URIs. |
| `AZICURE_TOTP_DIGITS` | `6` | Number of digits generated for TOTP tokens. |
| `AZICURE_TOTP_STEP` | `30` | Token validity period in seconds. |

Adjust these variables to point to secure storage locations in production.

## CLI quickstart

All CLI commands are available through the `azicure` console script or by
invoking the module directly with `python -m azicure.cli`. The sequence below
bootstraps a new environment, enrolls a device, and performs a full encrypt →
decrypt cycle.

1. **Generate (or load) the master key.**
   ```bash
   azicure keygen
   # or: python -m azicure.cli keygen
   ```
2. **Enroll a trusted device.**
   ```bash
   azicure device add --id my-laptop
   ```
3. **Initialize TOTP for an operator account.**
   ```bash
   azicure totp init --account alice@example.com
   ```
   The command prints a provisioning URI. Scan it with your authenticator app
   to capture the shared secret. Most apps also display the base32 secret in
   case you need to store it for API requests.
4. **Verify a TOTP token (optional sanity check).**
   ```bash
   azicure totp verify --secret <BASE32_SECRET> --token 123456
   ```
5. **Encrypt a document.**
   ```bash
   azicure encrypt ./data/plan.pdf ./data/plan.pdf.enc --aad "proposal"
   ```
6. **Decrypt the document.**
   ```bash
   azicure decrypt ./data/plan.pdf.enc ./data/plan.pdf.dec --aad "proposal"
   ```
7. **Manage tamper manifests.**
   ```bash
   azicure tamper build --paths data/plan.pdf.enc
   azicure tamper verify
   ```

## Running the FastAPI service

1. Complete the CLI bootstrapping steps above so a master key, whitelisted
   device ID, and enrolled TOTP secret exist.
2. Start the API server from the repository root (virtual environment active):
   ```bash
   uvicorn azicure.server.app:app --reload --port 8080
   ```
3. Issue requests with the enrolled credentials. Example encryption request:
   ```bash
   curl -X POST http://localhost:8080/encrypt \
     -H "Content-Type: application/json" \
     -d '{
           "src_path": "data/plan.pdf",
           "dst_path": "data/plan.api.enc",
           "aad": "proposal",
           "device_id": "my-laptop",
           "totp_secret": "<BASE32_SECRET>",
           "totp_token": "123456"
         }'
   ```
   Replace `totp_token` with the current code from your authenticator. Use the
   `/decrypt` endpoint with the same JSON schema to reverse the operation.

## Running tests

After installing Azicure in editable mode, run the test suite from the project
root:

```bash
pytest
```

The tests validate that the package can be imported when installed into the
active environment.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'azicure'`:** Ensure you installed the
  project with `pip install -e .` inside your virtual environment before running
  the CLI, API, or tests.
- **Authenticator cannot scan the URI:** Copy the provisioning URI into a QR
  code generator or manually input the base32 secret exposed by your
  authenticator application.
- **Permission issues writing configs:** Update the configuration environment
  variables to point to directories where the running user has read/write access.

With these steps you should be able to launch Azicure locally, enroll devices,
issue TOTP-protected encryption requests, and extend the system for your
organization’s security needs.
