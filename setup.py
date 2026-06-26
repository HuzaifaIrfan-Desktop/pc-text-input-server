

import ipaddress
import socket
from pathlib import Path

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta, timezone


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("1.1.1.1", 80))
        return s.getsockname()[0]
    finally:
        s.close()


ip = get_local_ip()

ssl_dir = Path("ssl")
ssl_dir.mkdir(exist_ok=True)

# Generate private key
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Certificate subject/issuer
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, ip),
])

# Subject Alternative Names
san = x509.SubjectAlternativeName([
    x509.IPAddress(ipaddress.ip_address(ip)),
    x509.DNSName("localhost"),
])

# Build certificate
cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.now(timezone.utc))
    .not_valid_after(datetime.now(timezone.utc) + timedelta(days=3650))
    .add_extension(san, critical=False)
    .sign(key, hashes.SHA256())
)

# Save private key
with open(ssl_dir / "key.pem", "wb") as f:
    f.write(
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        )
    )

# Save certificate
with open(ssl_dir / "cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print(f"Generated certificate for {ip}")
print("Certificate:", ssl_dir / "cert.pem")
print("Private key:", ssl_dir / "key.pem")





import json
import os
import platform
import secrets
import socket
import subprocess
from pathlib import Path

import qrcode

BASE = Path(__file__).parent
SSL = BASE / "ssl"

ENV_FILE = BASE / ".env"
QR_FILE = BASE / "pairing_qr.png"
PAIRING_FILE = BASE / "pairing_json.json"
CERT_FILE = SSL / "cert.pem"



import socket

PREFERRED_PORT = 51237


def get_available_port(preferred=PREFERRED_PORT):
    # Try preferred port first
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("0.0.0.0", preferred))
            return preferred
        except OSError:
            pass

    # Otherwise let the OS choose a free port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", 0))
        return s.getsockname()[1]
    
PORT = get_available_port()
from cryptography import x509
from cryptography.hazmat.primitives import hashes

def get_fingerprint():
    with open(CERT_FILE, "rb") as f:
        cert = x509.load_pem_x509_certificate(f.read())

    return cert.fingerprint(hashes.SHA256()).hex()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "127.0.0.1"
    finally:
        s.close()


from datetime import datetime, timezone

CREATED_ON=datetime.now(timezone.utc).isoformat()

def save_env(host, port, secret_key, pair_token, fingerprint):
    ENV_FILE.write_text(f"""HOST={host}
PORT={port}

CREATED_ON={CREATED_ON}
SECRET_KEY={secret_key}
PAIR_TOKEN={pair_token}

CERT_FINGERPRINT={fingerprint}

""")



def create_json_qr(host, port, pair_token, fingerprint):
    data = {
        "createdOn": CREATED_ON,
        "version": 1,
        "host": host,
        "port": port,
        "pairToken": pair_token,
        "fingerprint": fingerprint,
    }


    with open(PAIRING_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)   

    img = qrcode.make(json.dumps(data, separators=(",", ":")))
    img.save(QR_FILE)


def open_image():
    system = platform.system()

    if system == "Windows":
        os.startfile(QR_FILE)

    elif system == "Darwin":
        subprocess.run(["open", str(QR_FILE)])

    else:
        subprocess.run(["xdg-open", str(QR_FILE)])


def main():
    host = get_local_ip()

    secret_key = secrets.token_hex(32)      # 256-bit
    pair_token = secrets.token_hex(32)      # 256-bit

    fingerprint = get_fingerprint()

    save_env(
        host,
        PORT,
        secret_key,
        pair_token,
        fingerprint,
    )

    create_json_qr(
        host,
        PORT,
        pair_token,
        fingerprint,
    )

    print(".env created")
    print("QR code created:", QR_FILE)

    open_image()


if __name__ == "__main__":
    main()