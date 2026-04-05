# app/broker/crypto.py
#
# Symmetric encryption helper for broker credentials stored at rest.
# Uses Fernet (AES-128-CBC + HMAC-SHA256) from the `cryptography` package.
#
# Required env var:
#   BROKER_ENCRYPTION_KEY — a Fernet key generated once:
#     python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
#   Store this in Railway Variables. Never commit it to git.

import os
from cryptography.fernet import Fernet


def _fernet() -> Fernet:
    key = os.environ.get("BROKER_ENCRYPTION_KEY")
    if not key:
        raise RuntimeError(
            "BROKER_ENCRYPTION_KEY is not set. "
            "Generate one with: python3 -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
        )
    return Fernet(key.encode())


def encrypt(plaintext: str) -> str:
    """Encrypt a plaintext string. Returns a URL-safe base64 token."""
    return _fernet().encrypt(plaintext.encode()).decode()


def decrypt(ciphertext: str) -> str:
    """Decrypt a token produced by encrypt(). Raises InvalidToken on tamper."""
    return _fernet().decrypt(ciphertext.encode()).decode()
