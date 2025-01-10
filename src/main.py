import os
import json
import glob
from datetime import datetime
from utils.json_utils import load_json
from utils.excel_utils import write_to_excel
from processors import (
    ec2_processor, rds_processor, s3_processor, 
    elasticache_processor, kms_processor, lambda_processor, 
    elb_processor, eks_processor
)

def load_column_mapping(config_path):
    """
    Load column mapping configuration from a JSON file.
    """
    with open(config_path, 'r') as f:
        return json.load(f)

def find_json_files(base_dir, file_name):
    """
    Recursively search for a specific JSON file in the base directory.
    Returns the path if found, or None if not found.
    """
    search_pattern = os.path.join(base_dir, "**", file_name)
    matching_files = glob.glob(search_pattern, recursive=True)
    return matching_files[0] if matching_files else None

def detect_cloud_provider(aws_json_files, gcp_json_files, azure_json_files, aws_enabled, gcp_enabled, azure_enabled):
    """
    Detect the cloud provider by checking for the presence of JSON files.
    """
    detected_provider = None

    if aws_enabled:
        print("Checking AWS JSON files...")
        for key, path in aws_json_files.items():
            print(f"Checking path: {path}")
            if path and os.path.exists(path):
                print(f"AWS JSON file found: {path}")
                detected_provider = "aws"
        if not detected_provider:
            print("No AWS JSON files found.")

    if gcp_enabled:
        print("Checking GCP JSON files...")
        for key, path in gcp_json_files.items():
            print(f"Checking path: {path}")
            if path and os.path.exists(path):
                print(f"GCP JSON file found: {path}")
                detected_provider = "gcp"
        if not detected_provider:
            print("No GCP JSON files found.")

    if azure_enabled:
        print("Checking Azure JSON files...")
        for key, path in azure_json_files.items():
            print(f"Checking path: {path}")
            if path and os.path.exists(path):
                print(f"Azure JSON file found: {path}")
                detected_provider = "azure"
        if not detected_provider:
            print("No Azure JSON files found.")
    
    if not detected_provider:
        raise ValueError("No JSON files found for any enabled cloud provider.")
    return detected_provider

def get_most_recent_directory(base_path):
    """
    Find the most recent subdirectory in the base path.
    """
    subdirs = [os.path.join(base_path, d) for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    if not subdirs:
        raise ValueError(f"No subdirectories found in {base_path}")
    latest_subdir = max(subdirs, key=os.path.getmtime)
    return latest_subdir

def main():
    # Configuration paths
    column_mapping_path = "config/column_mapping.json"
    base_path = "data/json/aws/"
    
    try:
        most_recent_dir = get_most_recent_directory(base_path)
        print(f"Most recent directory: {most_recent_dir}")
    except ValueError as e:
        print(e)
        return
    
    # Define expected JSON files
    aws_json_files = {
        "ec2": "ec2-describe_instances.json",
        "rds": "rds-describe_db_instances.json",
        "s3": "s3-list_buckets.json",
        "elasticache": "elasticache-describe_cache_clusters.json",
        "kms": "kms-list_keys.json",
        "lambda": "lambda-list_functions.json",
        "elb": "elbv2-describe_load_balancers.json",
        "eks": "eks-list_clusters.json"
    }
    
    # Search for JSON files in subdirectories
    aws_json_files = {
        key: find_json_files(most_recent_dir, file_name)
        for key, file_name in aws_json_files.items()
    }

    # Check if any files were found
    if not any(aws_json_files.values()):
        print(f"No JSON files found in {most_recent_dir}. Please ensure the files exist.")
        return

    # Enable or disable specific cloud providers
    aws_enabled = True
    gcp_enabled = False
    azure_enabled = False

    # Detect the cloud provider
    try:
        cloud_provider = detect_cloud_provider(
            aws_json_files, {}, {}, aws_enabled, gcp_enabled, azure_enabled
        )
    except ValueError as e:
        print(e)
        return

    # Process services and collect data frames
    processors = {
        "ec2": ec2_processor.process_ec2,
        "rds": rds_processor.process_rds,
        "s3": s3_processor.process_s3,
        "elasticache": elasticache_processor.process_elasticache,
        "kms": kms_processor.process_kms,
        "lambda": lambda_processor.process_lambda,
        "elb": elb_processor.process_elb,
        "eks": eks_processor.process_eks
    }

    column_mapping = load_column_mapping(column_mapping_path)

    data_frames = []
    for service, file_path in aws_json_files.items():
        if file_path:
            data = load_json(file_path)
            data_frames.append(processors[service](data))

    # Write consolidated data to Excel
    excel_template = "data/excel/SSP-Appendix-M-Integrated-Inventory-Workbook-Template.xlsx"
    current_date = datetime.now()
    output_dir = os.path.join("output", current_date.strftime("%Y"), current_date.strftime("%b"))
    os.makedirs(output_dir, exist_ok=True)

    write_to_excel(excel_template, data_frames, column_mapping, output_dir)
    print(f"Processing completed successfully for {cloud_provider}!")

if __name__ == "__main__":
    main()
