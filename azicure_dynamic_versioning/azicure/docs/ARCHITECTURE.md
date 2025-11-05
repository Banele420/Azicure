# Architecture Overview

Azicure is composed of modular layers:

- **Core Security**: Encryption (AES-GCM), MFA (TOTP), Device Whitelisting, Tamper Detection, Logging.
- **Interfaces**: CLI (now), REST API (FastAPI), future GUI (desktop + installers).
- **Ops**: Dockerized API, CI pipeline, environment handling, manifests and registries.

The security domain is intentionally small and explicit for auditability. Keys are envelope-encrypted using a master key kept out of repo.
