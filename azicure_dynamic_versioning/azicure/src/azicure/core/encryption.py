from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import keywrap
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from os import urandom
from ..utils.env import MASTER_KEY_FILE
from .logging_config import get_logger

logger = get_logger(__name__)

def _load_or_create_master_key() -> bytes:
    if MASTER_KEY_FILE.exists():
        return MASTER_KEY_FILE.read_bytes()
    key = urandom(32)  # 256-bit
    MASTER_KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
    MASTER_KEY_FILE.write_bytes(key)
    logger.warning("Master key file was missing. A new one has been created at %s", MASTER_KEY_FILE)
    return key

def _derive_data_key(context: bytes) -> bytes:
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=context)
    return hkdf.derive(urandom(32))

def wrap_data_key(data_key: bytes) -> bytes:
    master = _load_or_create_master_key()
    # RFC 3394 AES Key Wrap with default backend wrapped in a simple scheme
    wrapped = keywrap.aes_key_wrap(master, data_key)
    return wrapped

def unwrap_data_key(wrapped: bytes) -> bytes:
    master = _load_or_create_master_key()
    return keywrap.aes_key_unwrap(master, wrapped)

def encrypt_file(src: Path, dst: Path, aad: bytes = b"") -> Path:
    src_bytes = Path(src).read_bytes()
    data_key = _derive_data_key(aad or b"azicure-session")
    wrapped = wrap_data_key(data_key)
    nonce = urandom(12)
    aes = AESGCM(data_key)
    ct = aes.encrypt(nonce, src_bytes, aad)
    payload = b"AZI1" + nonce + len(wrapped).to_bytes(2, "big") + wrapped + ct
    Path(dst).write_bytes(payload)
    logger.info("Encrypted %s -> %s", src, dst)
    return Path(dst)

def decrypt_file(src: Path, dst: Path, aad: bytes = b"") -> Path:
    payload = Path(src).read_bytes()
    assert payload[:4] == b"AZI1", "Invalid Azicure payload"
    nonce = payload[4:16]
    wlen = int.from_bytes(payload[16:18], "big")
    wrapped = payload[18:18+wlen]
    ct = payload[18+wlen:]
    data_key = unwrap_data_key(wrapped)
    aes = AESGCM(data_key)
    pt = aes.decrypt(nonce, ct, aad)
    Path(dst).write_bytes(pt)
    logger.info("Decrypted %s -> %s", src, dst)
    return Path(dst)
