import os
import json
import glob
from datetime import datetime
from utils.json_utils import load_json, load_column_mapping
from utils.excel_utils import write_to_excel
from processors import (
    ec2_processor, rds_processor, s3_processor,
    elasticache_processor, kms_processor, lambda_processor,
    elb_processor, eks_processor
)

def load_aws_file_mapping(config_path):
    """
    Load AWS file mapping configuration from a JSON file.
    """
    with open(config_path, 'r') as f:
        return json.load(f)

def generate_file_name(entry):
    """
    Generate a file name based on the AWS JSON entry.
    Example: ec2-describe_route_tables.json
    """
    service = entry.get("service", "unknown_service")
    function = entry.get("function", "unknown_function")
    return f"{service}-{function}.json"

def find_json_files(base_dir, file_name):
    """
    Recursively search for a specific JSON file in the base directory.
    Returns the path if found, or None if not found.
    """
    search_pattern = os.path.join(base_dir, "**", file_name)
    matching_files = glob.glob(search_pattern, recursive=True)
    return matching_files[0] if matching_files else None

def get_most_recent_directory(base_path):
    """
    Find the most recent subdirectory in the base path.
    """
    subdirs = [os.path.join(base_path, d) for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    if not subdirs:
        raise ValueError(f"No subdirectories found in {base_path}")
    latest_subdir = max(subdirs, key=os.path.getmtime)
    return latest_subdir

def detect_cloud_provider(aws_json_files, gcp_json_files, azure_json_files, aws_enabled, gcp_enabled, azure_enabled):
    """
    Detect the cloud provider by checking for the presence of JSON files.
    """
    detected_provider = None

    if aws_enabled:
        for key, path in aws_json_files.items():
            if path and os.path.exists(path):
                detected_provider = "aws"
                break

    if not detected_provider and gcp_enabled:
        for key, path in gcp_json_files.items():
            if path and os.path.exists(path):
                detected_provider = "gcp"
                break

    if not detected_provider and azure_enabled:
        for key, path in azure_json_files.items():
            if path and os.path.exists(path):
                detected_provider = "azure"
                break

    if not detected_provider:
        raise ValueError("No JSON files found for any enabled cloud provider.")
    return detected_provider

def main():
    # Configuration paths
    aws_config_path = "config/aws.json"  # Path to the JSON configuration
    column_mapping_path = "config/column_mapping.json"
    base_path = "data/json/aws/"
    
        # Load AWS JSON file mappings
    try:
        aws_file_mappings = load_aws_file_mapping(aws_config_path)
    except FileNotFoundError:
        print(f"Configuration file {aws_config_path} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {aws_config_path}.")
        return

    try:
        most_recent_dir = get_most_recent_directory(base_path)
        print(f"Most recent directory: {most_recent_dir}")
    except ValueError as e:
        print(e)
        return
    
    # Generate file names and search for them
    aws_json_files = {
        generate_file_name(entry): find_json_files(most_recent_dir, generate_file_name(entry))
        for entry in aws_file_mappings
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

    # Define processors for known services
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
    for file_name, file_path in aws_json_files.items():
        if file_path:
            service = file_name.split("-")[0]  # Extract service from file name
            processor = processors.get(service)
            if processor:
                try:
                    data = load_json(file_path)
                    data_frames.append(processor(data))
                except Exception as e:
                    print(f"Error processing service '{service}': {e}")
            else:
                print(f"No processor found for service '{service}'. Skipping...")

    # Write consolidated data to Excel
    excel_template = "data/excel/SSP-Appendix-M-Integrated-Inventory-Workbook-Template.xlsx"
    current_date = datetime.now()
    output_dir = os.path.join("output", current_date.strftime("%Y"), current_date.strftime("%b"))
    os.makedirs(output_dir, exist_ok=True)

    write_to_excel(excel_template, data_frames, column_mapping, output_dir)
    print(f"Processing completed successfully for {cloud_provider}!")

if __name__ == "__main__":
    main()