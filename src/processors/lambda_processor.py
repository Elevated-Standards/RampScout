import pandas as pd

def process_lambda(data):
    """
    Process Lambda JSON data and return a DataFrame.

    :param data: List of Lambda functions from the JSON file.
    :return: A pandas DataFrame with Lambda asset data.
    """
    records = []
    for function in data:
        records.append({
            "unique_id": function.get("FunctionArn"),
            "dns_name": function.get("FunctionName"),
            "asset_type": "Lambda Function",
            "location": function.get("VpcConfig", {}).get("VpcId", "No VPC"),  # Defaults to "No VPC" if not present
            "function": function.get("Description", "No description available"),
            "software_name_version": function.get("Runtime"),
            "comments": f"Memory: {function.get('MemorySize')} MB, Timeout: {function.get('Timeout')} seconds"
        })
    return pd.DataFrame(records)
