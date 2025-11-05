import json
from pathlib import Path
from typing import Set
from ..utils.env import DEVICE_REGISTRY
from .logging_config import get_logger

logger = get_logger(__name__)

def _ensure_registry():
    DEVICE_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    if not DEVICE_REGISTRY.exists():
        DEVICE_REGISTRY.write_text(json.dumps({"devices": []}, indent=2))

def get_devices() -> Set[str]:
    _ensure_registry()
    data = json.loads(DEVICE_REGISTRY.read_text())
    return set(data.get("devices", []))

def add_device(device_id: str) -> None:
    _ensure_registry()
    data = json.loads(DEVICE_REGISTRY.read_text())
    if device_id not in data["devices"]:
        data["devices"].append(device_id)
        DEVICE_REGISTRY.write_text(json.dumps(data, indent=2))
        logger.info("Added device %s to registry", device_id)

def is_allowed(device_id: str) -> bool:
    return device_id in get_devices()
