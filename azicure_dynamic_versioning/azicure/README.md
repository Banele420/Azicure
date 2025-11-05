# Azicure v0.2 — Trust Infrastructure Release

Enterprise-hardened prototype for secure document management and device trust.
Adds: keystore abstractions (TPM/HSM/KMS-ready), PKI-signed registries/manifests,
OAuth2/JWT with RBAC, admin dashboard, background tamper watchdog, and SIEM sinks.

> **Note:** Some hardware backends are pluggable stubs here (TPM/HSM/KMS) with
> working file-based defaults. Replace with real providers for production.

## Quickstart
```bash
python -m pip install -e .[dev]
uvicorn azicure.server.app:app --reload --port 8080
```
