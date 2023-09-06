import analysis_certificate as ca
import analysis_dns as da
import analysis_features_extraction as fa

def extract_and_analyse_features(device_conf, ref_flag, act_flag):
    fa.extract_features(device_conf, ref_flag, act_flag)


def extract_and_analyse_certificates(device_conf, ref_flag, act_flag):
    ca.analyze_certificate_df(device_conf, ref_flag, act_flag)


def extract_and_analyze_dns(device_conf, ref_flag, act_flag):
    da.analyse_individual_dns_data(device_conf, ref_flag, act_flag)
    da.analyze_DNS_df(device_conf, ref_flag, act_flag)

def extract_and_analyse(device_conf, ref_flag, act_flag):
    extract_and_analyse_features(device_conf, ref_flag, act_flag)
    extract_and_analyse_certificates(device_conf, ref_flag, act_flag)
    extract_and_analyze_dns(device_conf, ref_flag, act_flag)
