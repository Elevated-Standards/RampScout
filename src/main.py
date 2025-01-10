import os
import json
from utils.json_utils import load_json
from utils.excel_utils import write_to_excel
from datetime import datetime
from processors import (
    ec2_processor, rds_processor, s3_processor, 
    elasticache_processor, kms_processor, lambda_processor, 
    elb_processor, eks_processor
)

import re
 
# Load column mapping from config
def load_column_mapping(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def detect_cloud_provider(aws_json_files, gcp_json_files, azure_json_files, gcp_enabled, azure_enabled):
    if any(os.path.exists(path) for path in aws_json_files.values()):
        return "aws"
    elif gcp_enabled and any(os.path.exists(path) for path in gcp_json_files.values()):
        return "gcp"
    elif azure_enabled and any(os.path.exists(path) for path in azure_json_files.values()):
        return "azure"
    else:
        raise ValueError("No JSON files found for any cloud provider.")

def get_most_recent_directory(base_path):
    subdirs = [os.path.join(base_path, d) for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    if not subdirs:
        raise ValueError(f"No subdirectories found in {base_path}")
    latest_subdir = max(subdirs, key=os.path.getmtime)
    return latest_subdir

def main():
    # Configuration paths
    column_mapping_path = "config/column_mapping.json"
    
    base_path = "data/json/"
    try:
        most_recent_dir = get_most_recent_directory(base_path)
    except ValueError as e:
        print(e)
        return
    
    aws_json_files = {
        "ec2": os.path.join(base_path, "aws/ec2-describe_instances.json"),
        "rds": os.path.join(base_path, "aws/rds-describe_db_instances.json"),
        "s3": os.path.join(base_path, "aws/s3-list_buckets.json"),
        "elasticache": os.path.join(base_path, "aws/elasticache-describe_cache_clusters.json"),
        "kms": os.path.join(base_path, "aws/kms-list_keys.json"),
        "lambda": os.path.join(base_path, "aws/lambda-list_functions.json"),
        "elb": os.path.join(base_path, "aws/elbv2-describe_load_balancers.json"),
        "eks": os.path.join(base_path, "aws/eks-list_clusters.json")
    }
    
    gcp_json_files = {
        "compute_instances": os.path.join(base_path, "gcp/gcp-list_instances.json"),
        "sql_instances": os.path.join(base_path, "gcp/gcp-list_sql_instances.json"),
        "storage_buckets": os.path.join(base_path, "gcp/gcp-list_buckets.json"),
        "redis_instances": os.path.join(base_path, "gcp/gcp-list_redis_instances.json"),
        "kms_keys": os.path.join(base_path, "gcp/gcp-list_crypto_keys.json"),
        "cloud_functions": os.path.join(base_path, "gcp/gcp-list_functions.json"),
        "load_balancers": os.path.join(base_path, "gcp/gcp-list_load_balancers.json"),
        "gke_clusters": os.path.join(base_path, "gcp/gcp-list_clusters.json")
    }
    
    azure_json_files = {
        "virtual_machines": os.path.join(base_path, "azure/azure-list_virtual_machines.json"),
        "sql_servers": os.path.join(base_path, "azure/azure-list_sql_servers.json"),
        "storage_accounts": os.path.join(base_path, "azure/azure-list_storage_accounts.json"),
        "redis": os.path.join(base_path, "azure/azure-list_redis_caches.json"),
        "key_vaults": os.path.join(base_path, "azure/azure-list_key_vaults.json"),
        "functions": os.path.join(base_path, "azure/azure-list_functions.json"),
        "load_balancers": os.path.join(base_path, "azure/azure-list_load_balancers.json"),
        "aks": os.path.join(base_path, "azure/azure-list_managed_clusters.json")
    }

    excel_template = "data/excel/SSP-Appendix-M-Integrated-Inventory-Workbook-Template.xlsx"
 
    current_date = datetime.now()
    output_dir = os.path.join("output", current_date.strftime("%Y"), current_date.strftime("%b"))
    os.makedirs(output_dir, exist_ok=True)

    # Enable or disable specific cloud providers
    gcp_enabled = False
    azure_enabled = False

    # Detect the cloud provider
    cloud_provider = detect_cloud_provider(aws_json_files, gcp_json_files, azure_json_files, gcp_enabled, azure_enabled)
    
    if cloud_provider == "aws":
        json_files = aws_json_files
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
    elif cloud_provider == "gcp" and gcp_enabled:
        raise NotImplementedError("GCP processing is currently toggled off.")
    elif cloud_provider == "azure" and azure_enabled:
        raise NotImplementedError("Azure processing is currently toggled off.")
    else:
        raise ValueError("No valid cloud provider enabled or detected.")

    # Load column mapping
    column_mapping = load_column_mapping(column_mapping_path)

    # Process services and collect data frames
    data_frames = []
    for service, file_path in json_files.items():
        if os.path.exists(file_path):
            data = load_json(file_path)
            data_frames.append(processors[service](data))

    # Write consolidated data to Excel
    write_to_excel(excel_template, data_frames, column_mapping, output_dir)
    print(f"Processing completed successfully for {cloud_provider}!")

if __name__ == "__main__":
    main()
    # Additional code to handle other cloud providers can be added here in the future