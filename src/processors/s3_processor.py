import pandas as pd

def process_s3(data):
    """
    Process S3 JSON data and return a DataFrame.

    :param data: List of S3 buckets from the JSON file.
    :return: A pandas DataFrame with S3 asset data.
    """
    records = []
    for bucket in data:
        records.append({
            "unique_id": bucket.get("Name"),
            "dns_name": bucket.get("Name"),
            "asset_type": "S3 Bucket",
            "location": "Unknown",  # AWS S3 bucket location may need a separate API call
            "function": "Storage",
            "comments": f"Creation date: {bucket.get('CreationDate')}" if bucket.get("CreationDate") else "No creation date available"
        })
    return pd.DataFrame(records)
