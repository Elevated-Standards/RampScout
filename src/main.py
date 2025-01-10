import os
import json
from utils.json_utils import load_json
from utils.excel_utils import write_to_excel
from processors import ec2_processor, rds_processor, s3_processor, elasticache_processor, kms_processor, lambda_processor, elb_processor, eks_processor

# Load column mapping from config
def load_column_mapping(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def main():
    # Configuration paths
    column_mapping_path = "config/column_mapping.json"
    json_files = {
        "ec2": "data/json/ec2-describe_instances.json",
        "rds": "data/json/rds-describe_db_instances.json",
        "s3": "data/json/s3-list_buckets.json",
        "elasticache": "data/json/elasticache-describe_cache_clusters.json",
        "kms": "data/json/kms-list_keys.json",
        "lambda": "data/json/lambda-list_functions.json",
        "elb": "data/json/elbv2-describe_load_balancers.json",
        "eks": "data/json/eks-list_clusters.json"
    }

    excel_template = "data/excel/SSP-Appendix-M-Integrated-Inventory-Workbook-Template.xlsx"
    output_dir = "output/"

    # Load column mapping
    column_mapping = load_column_mapping(column_mapping_path)

    # Process services and collect data frames
    data_frames = []
    for service, file_path in json_files.items():
        data = load_json(file_path)

        if service == "ec2":
            data_frames.append(ec2_processor.process_ec2(data))
        elif service == "rds":
            data_frames.append(rds_processor.process_rds(data))
        elif service == "s3":
            data_frames.append(s3_processor.process_s3(data))
        elif service == "elasticache":
            data_frames.append(elasticache_processor.process_elasticache(data))
        elif service == "kms":
            data_frames.append(kms_processor.process_kms(data))
        elif service == "lambda":
            data_frames.append(lambda_processor.process_lambda(data))
        elif service == "elb":
            data_frames.append(elb_processor.process_elb(data))
        elif service == "eks":
            data_frames.append(eks_processor.process_eks(data))

    # Write consolidated data to Excel
    write_to_excel(excel_template, data_frames, column_mapping, output_dir)
    print("Processing completed successfully!")

if __name__ == "__main__":
    main()
