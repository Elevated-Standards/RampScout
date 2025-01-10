import pandas as pd

def process_elasticache(data):
    """
    Process ElastiCache JSON data and return a DataFrame.

    :param data: List of ElastiCache clusters from the JSON file.
    :return: A pandas DataFrame with ElastiCache asset data.
    """
    records = []
    for cluster in data:
        records.append({
            "unique_id": cluster.get("CacheClusterId"),
            "ip_address": cluster.get("ConfigurationEndpoint", {}).get("Address"),
            "dns_name": cluster.get("ConfigurationEndpoint", {}).get("Address"),
            "asset_type": "ElastiCache Cluster",
            "hardware_model": cluster.get("CacheNodeType"),
            "location": cluster.get("PreferredAvailabilityZone"),
            "vlan_network_id": cluster.get("CacheSubnetGroupName"),
            "function": next((tag["Value"] for tag in cluster.get("TagList", []) if tag["Key"] == "Function"), None),
            "software_name_version": f"{cluster.get('Engine')} {cluster.get('EngineVersion')}",
            "comments": f"Cluster status: {cluster.get('CacheClusterStatus')}"
        })
    return pd.DataFrame(records)
