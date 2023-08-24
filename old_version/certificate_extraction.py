from datetime import datetime
import json
import pandas as pd
import ssl
import socket

from cryptography import x509
from cryptography.hazmat.backends import default_backend
import OpenSSL.crypto as crypto

import utility as util


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


def get_certificate_type(binary_cert):
    # Decode the certificate data and extract the certificate type
    certificate = crypto.load_certificate(crypto.FILETYPE_ASN1, binary_cert)

    # Check the Subject Alternative Names (SAN) for EV or OV indication
    san_extension = certificate.get_extension(2)
    if san_extension and b'EV' in san_extension.get_data():
        return "Extended Validation (EV)"
    elif san_extension and b'OID.2.5.4.97' in san_extension.get_data():
        return "Organization Validation (OV)"
    else:
        # If SAN is not present, check the organization name for OV indication
        organization_name = certificate.get_subject().organizationName
        if organization_name:
            return "Organization Validation (OV)"
        else:
            return "Domain Validation (DV)"


def generate_json(website_url, hostname, alt_subject, json_output_path, file_name):
    json_result = [{"URL: ": website_url, "Hostname: ": hostname}]
    alt_subject_list = [{"type": item[0], "value": item[1]} for item in alt_subject]
    json_result.append(alt_subject_list)

    output_file_path = f"{json_output_path}{hostname}_alt_name_info_{file_name}.json"

    with open(output_file_path, 'w') as json_file:
        json.dump(json_result, json_file, indent=4)


def extract_certificate_info(website_url, file_name, json_output_path):
    error_tag = "Connection Error"
    port = 443  # Default port for HTTPS is 443

    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
            type = get_certificate_type(cert_binary)

            # Get the SSL/TLS protocol version
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
            type = error_tag
            protocol_version = error_tag
            alt_subject = [error_tag]
            
        finally:
            ssock.close()

    # Create a pandas DataFrame
    data = {
        "Website": [website_url],
        "Hostname": [hostname],
        "Certificate Subject (Common Name)": [subject.get("commonName", "")],
        "Certificate Subject (Organization)": [subject.get("organizationName", "")],
        "Certificate Subject (Locality or City)": [subject.get("localityName", "")],
        "Certificate Subject (State or Province)": [subject.get('stateOrProvinceName', '')],
        "Certificate Subject (Country)": [subject.get("countryName", "")],
        "Certificate Subject (Business Category)": [subject.get("businessCategory", "")],
        "Certificate Subject (Serial No.)": [subject.get("serialNumber", "")],
        "Certificate Subject (Jurisdiction State)": [subject.get("jurisdictionState", "")],
        "Certificate Subject (Jurisdiction Locality)": [subject.get("jurisdictionLocality", "")],
        "Certificate Issuer (Country Name)": [issuer.get("countryName", "")],
        "Certificate Issuer (Organization Name)": [issuer.get("organizationName", "")],
        "Certificate Issuer (Organizational Unit Name)": [issuer.get("organizationalUnitName", "")],
        "Certificate Issuer (Common Name)": [issuer.get("commonName", "")],
        "Certificate Version": [version],
        "Certificate Valid From": [not_before],
        "Certificate Valid Until": [not_after],
        "Certificate Valid Duration": [valid_period],
        "Certificate Serial Number": [serial_number],
        "Certificate Signature Algorithm": [signature_algorithm],
        "SSL/TLS Protocol Version": [protocol_version],
        "Certificate Type": [type],
        "Num of Certificate Alternate Subject Name": [len(alt_subject)],
        # "Certificate Alternate Subject Name": [alt_subject],
    }

    generate_json(website_url, hostname, alt_subject, json_output_path, file_name)
    

    df = pd.DataFrame(data)
    df.drop_duplicates(subset=["Website"], keep="last", inplace=True)

    return df



def extract_certificates(file_name, base_folder_name, urls):
    print("\nExtracting Certificate Data...")
    # Create an empty DataFrame to store the certificate information
    df_all = pd.DataFrame()

    json_output_path = f'{base_folder_name}/{util.OUTPUT_PATH_JSON_CERTS}'

    # Iterate over the URLs and extract the certificate information
    for url in urls:
        if url == util.ERROR_URL_FLAG:
            continue

        df = extract_certificate_info(url, file_name, json_output_path)
        df_all = pd.concat([df_all, df], ignore_index=True)
        print("<" + url + ">" + " done!")

    # Save the DataFrame to a file (e.g., CSV)
    output_file = f"{base_folder_name}/{util.OUTPUT_PATH_EXCEL_CERTS}{file_name}_certs.xlsx"
    df_all.to_excel(output_file, index=False)

    print("Certificate data extracted...")