# Azicure

A secure document management prototype with local key encryption, MFA (TOTP), device whitelisting, tamper detection, structured logging, and an optional FastAPI service. This is a *founder-friendly* starter repo you can push to GitHub immediately and extend into full GUI installers and cloud deployments.

## Highlights
- Local AES‑GCM file encryption with per‑session keys and envelope key storage.
- Time‑based One‑Time Passwords (TOTP) for MFA.
- Device whitelisting via signed device registry.
- Tamper detection using SHA‑256 digests for critical files.
- Structured logging with rotating file handlers.
- REST API via FastAPI + Docker.
- Test scaffold (pytest) + GitHub Actions CI.
- Docs including Founder’s Quickstart and Architecture Overview.

> **Note**: This is a prototype. Review and harden before production.

## Founder’s Quickstart
```bash
# 1) Create virtual env & install deps
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt

# 2) Create a .env (or export vars) for secrets
cp .env.example .env
# edit .env with your settings

# 3) Run CLI
python -m azicure.cli --help

# 4) Run API
uvicorn azicure.server.app:app --reload --port 8080
```

## Docker (API)
```bash
docker compose up --build
```

## Tests
```bash
pytest -q
```

## Security Notes
- Use OS‑level secret storage or HSM/KMS for master keys.
- Rotate keys regularly; audit logs; enforce least privilege.
- Validate device whitelist signatures off-box if possible.
- Review code paths that handle secrets; avoid printing secrets.
- Consider TPM/TEE binding for device identity in production.

## Project Layout
```
src/azicure/
  core/
    encryption.py
    totp.py
    whitelist.py
    tamper.py
    logging_config.py
  server/
    app.py
  gui/
    README.md
  utils/
    env.py
  cli.py
configs/
docs/
docker/
.github/workflows/ci.yml
installers/
tests/
```

---

© MIT License. See `LICENSE`.
