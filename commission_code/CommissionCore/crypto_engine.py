from cryptography.fernet import Fernet
import os

def generate_aes_key():
    """Generates a new AES key for encrypting the signature file."""
    key = Fernet.generate_key()
    os.makedirs("CommissionCore/secure_store", exist_ok=True)
    with open("CommissionCore/secure_store/aes.key", "wb") as f:
        f.write(key)
    return key

def load_aes_key():
    """Loads the AES key from storage."""
    with open("CommissionCore/secure_store/aes.key", "rb") as f:
        return f.read()

def encrypt_data(data: bytes) -> bytes:
    """Encrypts any given data using the stored AES key."""
    key = load_aes_key()
    cipher = Fernet(key)
    return cipher.encrypt(data)

def decrypt_data(token: bytes) -> bytes:
    """Decrypts an encrypted data token."""
    key = load_aes_key()
    cipher = Fernet(key)
    return cipher.decrypt(token)