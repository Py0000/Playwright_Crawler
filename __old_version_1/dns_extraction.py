import dns.resolver
import json
import utility as util
import pandas as pd
import os

NO_RECORDS_FLAG = "No records found"
TIMEOUT = "DNS resolution timed out"
DNS_EXCEPTION = "DNS Exception occurred"
ERROR_RESULTS = [[NO_RECORDS_FLAG], [TIMEOUT], [DNS_EXCEPTION]]

def get_A_records(domain, resolver):
    record_type = 'A'
    a_records = {
        'IPv4 Address (Value)': []
    }

    try:
        response = resolver.resolve(domain, record_type)

        for rdata in response:
            value = str(rdata)
            a_records['IPv4 Address (Value)'].append(value)
        
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        # If no records of the specified type are found, move on to the next record type
        a_records = [NO_RECORDS_FLAG]
    except (dns.resolver.LifetimeTimeout, dns.resolver.Timeout):
        a_records = [TIMEOUT]
    except Exception:
        a_records = [DNS_EXCEPTION]

    return a_records


def get_AAAA_records(domain, resolver):
    record_type = 'AAAA'
    aaaa_records = {
        'IPv6 Address (Value)': []
    }

    try:
        response = resolver.resolve(domain, record_type)

        for rdata in response:
            value = str(rdata)
            aaaa_records['IPv6 Address (Value)'].append(value)
        
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        # If no records of the specified type are found, move on to the next record type
        aaaa_records = [NO_RECORDS_FLAG]
    except (dns.resolver.LifetimeTimeout, dns.resolver.Timeout):
        aaaa_records = [TIMEOUT]
    except Exception:
        aaaa_records = [DNS_EXCEPTION]

    return aaaa_records



def get_CAA_records(domain, resolver):
    record_type = 'CAA'
    caa_records = {
        'Flag': [],
        'Tag': [],
        'Value': [],
    }

    try:
        response = resolver.resolve(domain, record_type)

        for rdata in response:
            caa_flag = rdata.caa_flag
            caa_tag = rdata.caa_tag.decode()
            caa_value = rdata.caa_value.decode()

            caa_records['Flag'].append(caa_flag)
            caa_records['Tag'].append(caa_tag)
            caa_records['Value'].append(caa_value)
  
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        # If no records of the specified type are found, move on to the next record type
        caa_records = [NO_RECORDS_FLAG]
    except (dns.resolver.LifetimeTimeout, dns.resolver.Timeout):
        caa_records = [TIMEOUT]
    except Exception:
        caa_records = [DNS_EXCEPTION]

    return caa_records



def get_CNAME_records(domain, resolver):
    record_type = 'CNAME'
    cname_records = {
        'Host Name Alias': [],
    }

    try:
        response = resolver.resolve(domain, record_type)

        for rdata in response:
            value = str(rdata)

            cname_records['Host Name Alias'].append(value)

    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        # If no records of the specified type are found, move on to the next record type
        cname_records = [NO_RECORDS_FLAG]
    except (dns.resolver.LifetimeTimeout, dns.resolver.Timeout):
        cname_records = [TIMEOUT]
    except Exception:
        cname_records = [DNS_EXCEPTION]

    return cname_records


def get_MX_records(domain, resolver):
    record_type = 'MX'
    mx_records = {
        'Preference': [],
        'Exchange': [],
    }

    try:
        response = resolver.resolve(domain, record_type)

        for rdata in response:
            priority = rdata.preference
            target = str(rdata.exchange)

            mx_records['Preference'].append(priority)
            mx_records['Exchange'].append(target)

    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        # If no records of the specified type are found, move on to the next record type
        mx_records = [NO_RECORDS_FLAG]
    except (dns.resolver.LifetimeTimeout, dns.resolver.Timeout):
        mx_records = [TIMEOUT]
    except Exception:
        mx_records = [DNS_EXCEPTION]

    return mx_records


def get_NS_records(domain, resolver):
    record_type = 'NS'
    ns_records = {
        'Name Server': [],
    }

    try:
        response = resolver.resolve(domain, record_type)

        for rdata in response:
            value = str(rdata)

            ns_records['Name Server'].append(value)

    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        # If no records of the specified type are found, move on to the next record type
        ns_records = [NO_RECORDS_FLAG]
    except (dns.resolver.LifetimeTimeout, dns.resolver.Timeout):
        ns_records = [TIMEOUT]
    except Exception:
        ns_records = [DNS_EXCEPTION]

    return ns_records

def get_SOA_records(domain, resolver):
    record_type = 'SOA'
    soa_records = {
        'MNAME': [],
        'RNAME': [],
        'SERIAL': [],
        'REFRESH': [],
        'RETRY': [],
        'EXPIRE': [],
        'MINIMUM': [],
    }

    try:
        response = resolver.resolve(domain, record_type)

        for rdata in response:
            mname = str(rdata.mname)
            rname = str(rdata.rname)
            serial = rdata.serial
            refresh = rdata.refresh
            retry = rdata.retry
            expire = rdata.expire
            minimum = rdata.minimum

            soa_records['MNAME'].append(mname)
            soa_records['RNAME'].append(rname)
            soa_records['SERIAL'].append(serial)
            soa_records['REFRESH'].append(refresh)
            soa_records['RETRY'].append(retry)
            soa_records['EXPIRE'].append(expire)
            soa_records['MINIMUM'].append(minimum)


    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        # If no records of the specified type are found, move on to the next record type
        soa_records = [NO_RECORDS_FLAG]
    except (dns.resolver.LifetimeTimeout, dns.resolver.Timeout):
        soa_records = [TIMEOUT]
    except Exception:
        soa_records = [DNS_EXCEPTION]

    return soa_records



def get_TXT_records(domain, resolver):
    record_type = 'TXT'
    txt_records = {
        'Text Data': [],
    }

    try:
        response = resolver.resolve(domain, record_type)

        for rdata in response:
            text_data = ' '.join([item.decode() for item in rdata.strings])

            txt_records['Text Data'].append(text_data)

    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        # If no records of the specified type are found, move on to the next record type
        txt_records = [NO_RECORDS_FLAG]
    except (dns.resolver.LifetimeTimeout, dns.resolver.Timeout):
        txt_records = [TIMEOUT]
    except Exception:
        txt_records = [DNS_EXCEPTION]

    return txt_records


def get_dns_records(domain):
    # Create a DNS resolver object
    resolver = dns.resolver.Resolver()

    a_records = get_A_records(domain, resolver)
    aaaa_records = get_AAAA_records(domain, resolver)
    caa_records = get_CAA_records(domain, resolver)
    cname_records = get_CNAME_records(domain, resolver)
    mx_records = get_MX_records(domain, resolver)
    ns_records = get_NS_records(domain, resolver)
    soa_records = get_SOA_records(domain, resolver)
    txt_records = get_TXT_records(domain, resolver)

    dns_records = {
        'Domain': domain,
        'A': a_records,
        'AAAA': aaaa_records,
        'CAA': caa_records,
        'CNAME': cname_records,
        'MX': mx_records,
        'NS': ns_records,
        'SOA': soa_records,
        'TXT': txt_records
    }

    return dns_records


def generate_dns_into_excel(summary_output_path, file_date, domain, records):
    has_A_records = True if records.get("A") not in ERROR_RESULTS else False
    has_AAAA_records = True if records.get("AAAA") not in ERROR_RESULTS else False
    has_CAA_records = True if records.get("CAA") not in ERROR_RESULTS else False
    has_CNAME_records = True if records.get("CNAME") not in ERROR_RESULTS else False
    has_MX_records = True if records.get("MX") not in ERROR_RESULTS else False
    has_NS_records = True if records.get("NS") not in ERROR_RESULTS else False
    has_SOA_records = True if records.get("SOA") not in ERROR_RESULTS else False
    has_TXT_records = True if records.get("TXT") not in ERROR_RESULTS else False
 
    data = {
        "Domain": [domain],
        "has_A_records": [has_A_records],
        "has_AAAA_records": [has_AAAA_records],
        "has_CAA_records": [has_CAA_records],
        "has_CNAME_records": [has_CNAME_records],
        "has_MX_records": [has_MX_records],
        "has_NS_records": [has_NS_records],
        "has_SOA_records": [has_SOA_records],
        "has_TXT_records": [has_TXT_records],
    }

    save_loc = f"{summary_output_path}{file_date}_summary.xlsx"
    if os.path.isfile(save_loc):
        # Load the existing DataFrame from the Excel file
        existing_df = pd.read_excel(save_loc)
        
        # Append the new data to the existing DataFrame
        df = pd.concat([existing_df, pd.DataFrame(data)], ignore_index=True)
    else:
        # Create a new DataFrame with the data if the file doesn't exist
        df = pd.DataFrame(data)

    df.drop_duplicates(subset=["Domain"], keep="last", inplace=True)
    df.to_excel(save_loc, index=False)


def generate_dns_records(file_name, base_folder_name, urls):    
    print("\nExtracting DNS Data...")
    summary_output_path = f"{base_folder_name}/{util.OUTPUT_PATH_DNS}"

    for url in urls:
        if url == util.ERROR_URL_FLAG:
            continue
        
        domain = util.extract_hostname(url)
        if domain is None:
            continue
        
        records = get_dns_records(domain)

        generate_dns_into_excel(summary_output_path, file_name, domain, records)

        save_loc = f"{base_folder_name}/{util.OUTPUT_PATH_DNS}{domain}_dns_records_{file_name}.json"

        with open(save_loc, 'w') as file:
            json.dump(records, file, indent=4)
        
        print("Domain (" + domain + ") done!")
    
    print("DNS data extracted...")