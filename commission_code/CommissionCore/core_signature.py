import hashlib
import json
import os
from datetime import datetime
from crypto_engine import generate_aes_key, encrypt_data, decrypt_data

CONFIG_PATH = "CommissionCore/project_config.json"

def generate_signature():
    """Generates a 256-bit SHA key for your project and encrypts it."""
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    # Add timestamp and serialize
    config["generated"] = str(datetime.now())
    data_str = json.dumps(config, sort_keys=True).encode()

    # Create SHA256 digest
    dex_hash = hashlib.sha256(data_str).hexdigest()

    # Create encrypted record
    generate_aes_key()
    encrypted = encrypt_data(dex_hash.encode())

    os.makedirs("CommissionCore/secure_store", exist_ok=True)
    with open("CommissionCore/secure_store/key.bin", "wb") as f:
        f.write(encrypted)

    print(f"✅ Encrypted 256-bit project key generated and stored.")
    return dex_hash


def verify_signature():
    """Verifies the integrity of the stored key."""
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    data_str = json.dumps(config, sort_keys=True).encode()
    expected_hash = hashlib.sha256(data_str).hexdigest()

    with open("CommissionCore/secure_store/key.bin", "rb") as f:
        encrypted_key = f.read()

    decrypted_hash = decrypt_data(encrypted_key).decode()

    if decrypted_hash == expected_hash:
        print("✅ Verification Successful — Project Signature Valid.")
    else:
        print("❌ Verification Failed — Signature Mismatch.")


if __name__ == "__main__":
    print("CommissionCore v1.0 — Universal Signature Generator")
    action = input("Generate (G) or Verify (V)? ").strip().lower()
    if action == "g":
        generate_signature()
    elif action == "v":
        verify_signature()
    else:
        print("Invalid input.")
