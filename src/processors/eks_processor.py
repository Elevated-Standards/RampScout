import pandas as pd

def process_eks(data):
    """
    Process EKS JSON data and return a DataFrame.

    :param data: List of EKS clusters from the JSON file.
    :return: A pandas DataFrame with EKS asset data.
    """
    records = []
    for cluster_name in data:
        records.append({
            "unique_id": f"arn:aws:eks:{cluster_name}",
            "dns_name": cluster_name,
            "asset_type": "EKS Cluster",
            "function": "Container Orchestration",
            "comments": "Elastic Kubernetes Service Cluster"
        })
    return pd.DataFrame(records)
