import boto3
import json
import os
from datetime import datetime

# Define the AWS service configuration
AWS_SERVICES = [
    {
        "function": "describe_repositories",
        "result_key": "repositories",
        "service": "ecr",
        "fields": ["repositoryName", "repositoryArn", "repositoryUri", "createdAt", "tags"]
    },
    {
        "function": "describe_instances",
        "parameters": {
            "Filters": [
                {
                    "Name": "instance-state-name",
                    "Values": ["running"]
                }
            ]
        },
        "result_key": "Reservations",
        "service": "ec2",
        "fields": ["instanceId", "instanceType", "keyName", "state", "privateIpAddress", "publicIpAddress", "macAddress", "ami", "vpcId", "tags"]
    },
    {
        "function": "describe_db_instances",
        "result_key": "DBInstances",
        "service": "rds",
        "fields": ["dbInstanceIdentifier", "dbInstanceClass", "engine", "endpoint", "status", "createdAt", "vpcId", "tags"]
    },
    {
        "function": "list_buckets",
        "result_key": "Buckets",
        "service": "s3",
        "fields": ["name", "creationDate", "region", "tags"]
    },
    {
        "function": "list_clusters",
        "result_key": "clusters",
        "service": "eks",
        "fields": ["name", "arn", "status", "version", "vpcConfig", "tags"]
    },
    {
        "function": "list_clusters",
        "result_key": "clusterArns",
        "service": "ecs",
        "fields": ["clusterName", "clusterArn", "status", "runningTasksCount", "pendingTasksCount", "tags"]
    },
    {
        "function": "list_keys",
        "result_key": "Keys",
        "service": "kms",
        "fields": ["keyId", "keyArn", "creationDate", "description", "keyUsage", "keyState", "tags"]
    },
    {
        "function": "describe_load_balancers",
        "result_key": "LoadBalancers",
        "service": "elbv2",
        "fields": ["loadBalancerName", "loadBalancerArn", "DNSName", "scheme", "vpcId", "state", "type", "tags"]
    },
    {
        "function": "list_functions",
        "result_key": "Functions",
        "service": "lambda",
        "fields": ["functionName", "functionArn", "runtime", "handler", "memorySize", "timeout", "lastModified", "tags"]
    },
    {
        "function": "list_tables",
        "result_key": "TableNames",
        "service": "dynamodb",
        "fields": ["tableName", "tableArn", "creationDateTime", "itemCount", "tableSizeBytes", "tags"]
    },
    {
        "function": "describe_cache_clusters",
        "result_key": "CacheClusters",
        "service": "elasticache",
        "fields": ["cacheClusterId", "engine", "cacheNodeType", "numCacheNodes", "status", "endpoint", "tags"]
    }
]

# Ensure the output directory exists
OUTPUT_DIR = "data/json"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_and_save_data():
    """Fetch data from AWS services and save as JSON files."""
    session = boto3.Session()

    for service_config in AWS_SERVICES:
        service_name = service_config["service"]
        function_name = service_config["function"]
        result_key = service_config["result_key"]
        parameters = service_config.get("parameters", {})

        # Initialize the service client
        client = session.client(service_name)

        # Dynamically call the AWS function
        try:
            response = getattr(client, function_name)(**parameters)
            data = response.get(result_key, [])

            # File path for output
            output_file = os.path.join(OUTPUT_DIR, f"{service_name}-{function_name}.json")

            # Notify if overwriting an existing file
            if os.path.exists(output_file):
                print(f"Overwriting existing file: {output_file}")

            # Save data to a JSON file
            with open(output_file, "w") as f:
                json.dump(data, f, indent=4, default=str)

            print(f"Data for {service_name} ({function_name}) saved to {output_file}")
        except Exception as e:
            print(f"Error fetching data from {service_name} ({function_name}): {e}")

if __name__ == "__main__":
    fetch_and_save_data()
