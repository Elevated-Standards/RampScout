import pandas as pd

def process_ec2(data):
    """
    Process EC2 JSON data and return a DataFrame.

    :param data: List of EC2 reservations from the JSON file.
    :return: A pandas DataFrame with EC2 asset data.
    """
    records = []
    for reservation in data:
        for instance in reservation.get("Instances", []):
            records.append({
                "unique_id": instance.get("InstanceId"),
                "ip_address": instance.get("PrivateIpAddress"),
                "mac_address": instance.get("NetworkInterfaces", [{}])[0].get("MacAddress"),
                "dns_name": instance.get("PrivateDnsName"),
                "asset_type": "EC2",
                "hardware_model": instance.get("InstanceType"),
                "location": instance.get("Placement", {}).get("AvailabilityZone"),
                "vlan_network_id": instance.get("VpcId"),
                "function": next((tag["Value"] for tag in instance.get("Tags", []) if tag["Key"] == "Function"), None),
                "is_virtual": "Yes",
                "authenticated_scan_planned": "Yes"
            })
    return pd.DataFrame(records)
