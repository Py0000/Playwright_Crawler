import argparse

import faulty_data_filter 
import categorize_data

LABEL_BOTH_FAULTY_TXT_FILE = "_dual_faulty_dataset.txt"
LABEL_SELF_REF_FAULTY_TXT_FILE = "_self_ref_obly_faulty_dataset.txt"
LABEL_NO_REF_FAULTY_TXT_FILE = "_no_ref_obly_faulty_dataset.txt"

FAULTY_DIR_BOTH = "faulty_both"
FAULTY_DIR_SELF = "faulty_self_ref"
FAULTY_DIR_NO = "faulty_no_ref"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Supply the folder names")
    parser.add_argument("dataset", help="Name of dataset folder path")
    parser.add_argument("date", help="Date of dataset")
    args = parser.parse_args()

    dateset_date = args.date
    dataset_path = args.dataset

    print("\nFinding faulty dataset...")
    faulty_data_filter.filter_faulty_dataset(dataset_path, dateset_date)
    print("\nCategorizing both faulty dataset...")
    categorize_data.categorize(dateset_date, dataset_path, f"{dateset_date}{LABEL_BOTH_FAULTY_TXT_FILE}", FAULTY_DIR_BOTH)
    print("\nCategorizing self ref only faulty dataset...")
    categorize_data.categorize(dateset_date, dataset_path, f"{dateset_date}{LABEL_SELF_REF_FAULTY_TXT_FILE}", FAULTY_DIR_SELF)
    print("\nCategorizing no ref only faulty dataset...")
    categorize_data.categorize(dateset_date, dataset_path, f"{dateset_date}{LABEL_NO_REF_FAULTY_TXT_FILE}", FAULTY_DIR_NO)
    print("\nCleaning up complete data...")
    categorize_data.clean_up_complete_data(dataset_path)
    