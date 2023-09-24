import analysis_certificate as ca
import analysis_dns as da
import analysis_features_extraction as fa

import analysis_dom_comparison as dom_comparison
import analysis_page_detector as page_detector
import analysis_screenshot_comparison as screenshot_comparison



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


def analysis_page_for_differences(dataset_folder):
    dom_comparison.generate_dom_comparison_data(dataset_folder)
    page_detector.generate_page_analysis_report(dataset_folder)
    screenshot_comparison.generate_screenshot_comparison_report(dataset_folder)

