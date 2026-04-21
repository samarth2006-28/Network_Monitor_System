from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
import os

def generate_self_signed_cert():
    """Generates a private key and a self-signed certificate for SSL."""
    if os.path.exists("data/cert.pem"):
        return # Don't overwrite if it exists

    # Generate Private Key
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # Create Certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"IN"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Karnataka"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Bengaluru"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"PES University"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"nems-monitor.local"),
    ])

    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
        critical=False,
    ).sign(key, hashes.SHA256())

    # Write to files
    with open("data/key.pem", "wb") as f:
        f.write(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL, serialization.NoEncryption()))
    
    with open("data/cert.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    print("[*] SSL Certificate and Key generated in data/ folder.")