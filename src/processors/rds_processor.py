import pandas as pd

def process_rds(data):
    """
    Process RDS JSON data and return a DataFrame.

    :param data: List of RDS instances from the JSON file.
    :return: A pandas DataFrame with RDS asset data.
    """
    records = []
    for db_instance in data:
        records.append({
            "unique_id": db_instance.get("DBInstanceIdentifier"),
            "ip_address": db_instance.get("Endpoint", {}).get("Address"),
            "dns_name": db_instance.get("Endpoint", {}).get("Address"),
            "asset_type": "RDS",
            "hardware_model": db_instance.get("DBInstanceClass"),
            "location": db_instance.get("AvailabilityZone"),
            "vlan_network_id": db_instance.get("DBSubnetGroup", {}).get("VpcId"),
            "function": next((tag["Value"] for tag in db_instance.get("TagList", []) if tag["Key"] == "Function"), None),
            "software_name_version": f"{db_instance.get('Engine')} {db_instance.get('EngineVersion')}",
            "is_virtual": "Yes",
            "software_vendor": "AWS",
            "is_public": "Yes" if db_instance.get("PubliclyAccessible") else "No"
        })
    return pd.DataFrame(records)
