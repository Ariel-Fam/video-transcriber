# check_ssl.py

import ssl
import certifi




def main():
    print("=== SSL Certificate Paths ===")
    print(f"certifi CA bundle: {certifi.where()}")

    default_verify_paths = ssl.get_default_verify_paths()
    print(f"OpenSSL cafile: {default_verify_paths.openssl_cafile}")
    print(f"OpenSSL capath: {default_verify_paths.openssl_capath}")

    # Check if SSL_CERT_FILE is set
    import os
    ssl_cert_file = os.getenv('SSL_CERT_FILE')
    if ssl_cert_file:
        print(f"Environment Variable SSL_CERT_FILE: {ssl_cert_file}")
    else:
        print("Environment Variable SSL_CERT_FILE: Not Set")


if __name__ == "__main__":
    main()
