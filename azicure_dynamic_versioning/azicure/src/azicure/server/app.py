from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from ..core.encryption import encrypt_file, decrypt_file
from ..core.totp import verify as totp_verify
from ..core.whitelist import is_allowed
from ..core.logging_config import get_logger

app = FastAPI(title="Azicure API", version="0.1.0")
logger = get_logger(__name__)

class EncryptReq(BaseModel):
    src_path: str
    dst_path: str
    aad: str = ""
    device_id: str
    totp_secret: str
    totp_token: str

class DecryptReq(EncryptReq):
    pass

@app.post("/encrypt")
def encrypt(req: EncryptReq):
    if not is_allowed(req.device_id):
        raise HTTPException(status_code=403, detail="Device not whitelisted")
    if not totp_verify(req.totp_secret, req.totp_token):
        raise HTTPException(status_code=401, detail="Invalid TOTP")
    try:
        encrypt_file(Path(req.src_path), Path(req.dst_path), req.aad.encode())
    except Exception as e:
        logger.exception("Encrypt failed")
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "ok", "path": req.dst_path}

@app.post("/decrypt")
def decrypt(req: DecryptReq):
    if not is_allowed(req.device_id):
        raise HTTPException(status_code=403, detail="Device not whitelisted")
    if not totp_verify(req.totp_secret, req.totp_token):
        raise HTTPException(status_code=401, detail="Invalid TOTP")
    try:
        decrypt_file(Path(req.src_path), Path(req.dst_path), req.aad.encode())
    except Exception as e:
        logger.exception("Decrypt failed")
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "ok", "path": req.dst_path}
