from datetime import datetime
import json
import os

from cryptography import x509
from cryptography.hazmat.backends import default_backend
import ssl
import socket

import util
import util_def

def parse_date(date):
    # Convert the original date string to a datetime object
    dt = datetime.strptime(date, "%b %d %H:%M:%S %Y %Z")

    # Format the datetime object to the desired format
    formatted_date = dt.strftime("%b %d %Y")

    return formatted_date


def calc_duration(start, end):
    start = parse_date(start)
    end = parse_date(end)

    # Convert the date string to a datetime object
    start = datetime.strptime(start, "%b %d %Y").date()
    end = datetime.strptime(end, "%b %d %Y").date()

    num_days = (end - start).days
    return num_days



def get_certificate_signature_algorithm(cert):
    cert_object = x509.load_der_x509_certificate(cert, default_backend())
    signature_algorithm = cert_object.signature_algorithm_oid._name
    return signature_algorithm

    


def extract_certificate_info(website_url, folder_path):
    error_tag = "Connection Error"
    port = 443  # Default port for HTTPS is 443

    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Get the hostname from the url
    hostname = util.extract_hostname(website_url)
    if hostname is None:
        return
    
    # Wrap the socket with SSL/TLS
    context = ssl.create_default_context()
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        try:
            # Establish a connection to the website
            ssock.connect((hostname, port))

            # Get the TLS certificate information
            cert = ssock.getpeercert()
            cert_binary = ssock.getpeercert(binary_form=True)

            # Extract certificate details
            subject = dict(x[0] for x in cert["subject"])
            alt_subject= cert["subjectAltName"]
            issuer = dict(x[0] for x in cert["issuer"])
            version = cert["version"]
            not_before = cert["notBefore"]
            not_after = cert["notAfter"]
            valid_period = calc_duration(not_before, not_after)
            serial_number = cert["serialNumber"]
            signature_algorithm = get_certificate_signature_algorithm(cert_binary)
            protocol_version = ssock.version()

        except:
            subject = {
                "commonName": error_tag,
                "organizationName": error_tag,
                "localityName": error_tag,
                "stateOrProvinceName": error_tag,
                "countryName": error_tag,
                "businessCategory": error_tag,
                "serialNumber": error_tag,
                "jurisdictionState": error_tag,
                "jurisdictionLocality": error_tag,
            }

            issuer = {
                "countryName": error_tag,
                "organizationName": error_tag,
                "organizationalUnitName": error_tag,
                "commonName": error_tag,
            }
            version = error_tag 
            not_before = error_tag 
            not_after = error_tag 
            valid_period = error_tag 
            serial_number = error_tag 
            signature_algorithm = error_tag
            protocol_version = error_tag
            alt_subject = [error_tag]
            
        finally:
            ssock.close()
    
    data = {
        "website url": website_url,
        "hostname": hostname,
        "subject": subject,
        "issuer": issuer,
        "version": version,
        "not_before": not_before,
        "not after": not_after,
        "valid_period": valid_period,
        "serial_number": serial_number,
        "signature_algo": signature_algorithm,
        "protocol_version": protocol_version,
        "alternate subject name": alt_subject
    }

    with open(os.path.join(folder_path, util_def.TLS_CERT_FILE), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Certificate info saved... ")


