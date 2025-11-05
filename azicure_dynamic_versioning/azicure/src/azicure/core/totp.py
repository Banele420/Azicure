import pyotp
from ..utils.env import ISSUER, TOTP_DIGITS, TOTP_STEP
from .logging_config import get_logger

logger = get_logger(__name__)

def init_secret(account_name: str) -> str:
    secret = pyotp.random_base32()
    uri = pyotp.totp.TOTP(secret, digits=TOTP_DIGITS, interval=TOTP_STEP).provisioning_uri(name=account_name, issuer_name=ISSUER)
    logger.info("Generated new TOTP secret for %s", account_name)
    return uri  # User should scan this URI in an authenticator app

def verify(secret: str, token: str) -> bool:
    totp = pyotp.TOTP(secret, digits=TOTP_DIGITS, interval=TOTP_STEP)
    return totp.verify(token, valid_window=1)
