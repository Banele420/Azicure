import json, hashlib
from pathlib import Path
from typing import Dict
from ..utils.env import TAMPER_MANIFEST
from .logging_config import get_logger

logger = get_logger(__name__)

def _hash_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def build_manifest(paths) -> None:
    TAMPER_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    manifest: Dict[str, str] = {}
    for p in paths:
        pp = Path(p)
        if pp.is_file():
            manifest[str(pp)] = _hash_file(pp)
    TAMPER_MANIFEST.write_text(json.dumps(manifest, indent=2))
    logger.info("Built tamper manifest at %s", TAMPER_MANIFEST)

def verify_manifest() -> Dict[str, bool]:
    if not TAMPER_MANIFEST.exists():
        raise FileNotFoundError("Tamper manifest not found")
    manifest = json.loads(TAMPER_MANIFEST.read_text())
    results = {}
    for path, digest in manifest.items():
        pp = Path(path)
        results[path] = pp.exists() and _hash_file(pp) == digest
    return results
