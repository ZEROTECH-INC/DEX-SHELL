"""
key_generator.py

Generates RSA keypairs for license signing, and creates signed license tokens.
Requires: cryptography

Usage examples:
  python key_generator.py gen-keys --outdir ./keys --passphrase secret
  python key_generator.py sign --private ./keys/private_key.pem --payload license.json --out license.sig
  python key_generator.py verify --public ./keys/public_key.pem --payload license.json --sig license.sig

Notes:
- Keep the private key secure. Do NOT commit private_key.pem to VCS.
- The script includes a simple JSON license format and signs it using RSA-PSS (SHA256).
"""
import argparse
import json
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend


def gen_keys(outdir: Path, passphrase: str | None = None, key_size: int = 3072):
    outdir.mkdir(parents=True, exist_ok=True)
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size, backend=default_backend())

    # serialize private
    if passphrase:
        enc = serialization.BestAvailableEncryption(passphrase.encode())
    else:
        enc = serialization.NoEncryption()

    priv_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=enc,
    )
    pub = private_key.public_key()
    pub_bytes = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    priv_path = outdir / 'private_key.pem'
    pub_path = outdir / 'public_key.pem'
    priv_path.write_bytes(priv_bytes)
    pub_path.write_bytes(pub_bytes)
    print(f'Generated keys: {priv_path} (private), {pub_path} (public)')
    return priv_path, pub_path


def load_private_key(path: Path, passphrase: str | None = None):
    data = path.read_bytes()
    return serialization.load_pem_private_key(data, password=passphrase.encode() if passphrase else None, backend=default_backend())


def load_public_key(path: Path):
    data = path.read_bytes()
    return serialization.load_pem_public_key(data, backend=default_backend())


def sign_payload(private_key, payload_bytes: bytes) -> bytes:
    sig = private_key.sign(
        payload_bytes,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256(),
    )
    return sig


def verify_signature(public_key, payload_bytes: bytes, signature: bytes) -> bool:
    try:
        public_key.verify(
            signature,
            payload_bytes,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False


def make_license_payload(owner: str, expires: str | None = None, features: dict | None = None) -> dict:
    data = {
        'owner': owner,
        'issued_at': __import__('datetime').datetime.utcnow().isoformat() + 'Z',
        'expires': expires,
        'features': features or {},
        'product': 'DEX Shell',
        'version': '0.9.4-alpha',
    }
    return data


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest='cmd')

    gk = sub.add_parser('gen-keys')
    gk.add_argument('--outdir', default='keys')
    gk.add_argument('--passphrase', default=None)
    gk.add_argument('--keysize', default=3072, type=int)

    sign = sub.add_parser('sign')
    sign.add_argument('--private', required=True)
    sign.add_argument('--passphrase', default=None)
    sign.add_argument('--payload', required=True)
    sign.add_argument('--out', default='license.sig')

    verify = sub.add_parser('verify')
    verify.add_argument('--public', required=True)
    verify.add_argument('--payload', required=True)
    verify.add_argument('--sig', required=True)

    genlicense = sub.add_parser('gen-license')
    genlicense.add_argument('--owner', required=True)
    genlicense.add_argument('--expires', default=None)
    genlicense.add_argument('--out', default='license.json')

    args = p.parse_args()

    if args.cmd == 'gen-keys':
        gen_keys(Path(args.outdir), args.passphrase, args.keysize)

    elif args.cmd == 'sign':
        pk = load_private_key(Path(args.private), args.passphrase)
        payload = Path(args.payload).read_bytes()
        sig = sign_payload(pk, payload)
        Path(args.out).write_bytes(sig)
        print('Payload signed ->', args.out)

    elif args.cmd == 'verify':
        pub = load_public_key(Path(args.public))
        payload = Path(args.payload).read_bytes()
        sig = Path(args.sig).read_bytes()
        ok = verify_signature(pub, payload, sig)
        print('Signature valid' if ok else 'Signature INVALID')
        sys.exit(0 if ok else 2)

    elif args.cmd == 'gen-license':
        payload = make_license_payload(args.owner, args.expires)
        Path(args.out).write_text(json.dumps(payload, indent=2))
        print('License file written ->', args.out)

    else:
        p.print_help()


if __name__ == '__main__':
    main()