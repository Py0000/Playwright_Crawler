import analysis_certificate as ca
import analysis_dns as da
import analysis_features_extraction as fa

def extract_and_analyse_features(ref_flag):
    fa.extract_features(ref_flag)


def extract_and_analyse_certificates(ref_flag):
    ca.analyze_certificate_df(ref_flag)


def extract_and_analyze_dns(ref_flag):
    da.analyze_DNS_df(ref_flag)

def extract_and_analyse(ref_flag):
    extract_and_analyse_features(ref_flag)
    extract_and_analyse_certificates(ref_flag)
    extract_and_analyze_dns(ref_flag)
