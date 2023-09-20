import dns.resolver
import json
import os

import util
import util_def

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


def extract_dns_records(website_url, folder_path):
    domain = util.extract_hostname(website_url)

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

    with open(os.path.join(folder_path, util_def.DNS_FILE), 'w', encoding='utf-8') as f:
        json.dump(dns_records, f, ensure_ascii=False, indent=4)

    print("DNS info saved... ")
