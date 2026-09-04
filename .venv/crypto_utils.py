# crypto_utils.py
import base64
import json
import os
import uuid
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SALT = b"fin_track_salt_9988"
DATA_FILE = "budget_data.enc"

def _get_machine_token():
    # Генерирует уникальный ключ на основе железа ПК
    node = uuid.getnode()
    return f"key_fin_{node}".encode("utf-8")

def _get_cipher():
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100_000
    )
    return Fernet(base64.urlsafe_b64encode(kdf.derive(_get_machine_token())))

def save_data(data):
    cipher = _get_cipher()
    raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
    with open(DATA_FILE, "wb") as f:
        f.write(cipher.encrypt(raw))

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        cipher = _get_cipher()
        with open(DATA_FILE, "rb") as f:
            return json.loads(cipher.decrypt(f.read()).decode("utf-8"))
    except Exception:
        return []
