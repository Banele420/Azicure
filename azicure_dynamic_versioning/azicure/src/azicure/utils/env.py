from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

MASTER_KEY_FILE = Path(os.getenv("AZICURE_MASTER_KEY_FILE", "./configs/master_key.bin"))
DEVICE_REGISTRY = Path(os.getenv("AZICURE_DEVICE_REGISTRY", "./configs/device_registry.json"))
LOG_DIR = Path(os.getenv("AZICURE_LOG_DIR", "./logs"))
TAMPER_MANIFEST = Path(os.getenv("AZICURE_TAMPER_MANIFEST", "./configs/tamper_manifest.json"))
ISSUER = os.getenv("AZICURE_ISSUER", "Azicure")
TOTP_DIGITS = int(os.getenv("AZICURE_TOTP_DIGITS", "6"))
TOTP_STEP = int(os.getenv("AZICURE_TOTP_STEP", "30"))
