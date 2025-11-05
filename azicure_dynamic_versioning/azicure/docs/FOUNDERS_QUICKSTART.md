# Founder’s Quickstart

1. Clone and create a fresh virtual environment.
2. Copy `.env.example` to `.env` and customize paths.
3. Generate a master key: `python -m azicure.cli keygen`.
4. Register your device: `python -m azicure.cli device add --id <DEVICE_ID>`.
5. Create a TOTP secret: `python -m azicure.cli totp init` then enroll in authenticator.
6. Encrypt a doc: `python -m azicure.cli encrypt ./data/plan.pdf ./data/plan.enc`.
7. Decrypt to verify: `python -m azicure.cli decrypt ./data/plan.enc ./data/plan.dec.pdf`.
8. Start the API: `uvicorn azicure.server.app:app --reload --port 8080`.
