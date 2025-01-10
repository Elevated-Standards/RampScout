import pandas as pd

def process_elb(data):
    """
    Process ELB JSON data and return a DataFrame.

    :param data: List of ELB load balancers from the JSON file.
    :return: A pandas DataFrame with ELB asset data.
    """
    records = []
    for load_balancer in data:
        records.append({
            "unique_id": load_balancer.get("LoadBalancerArn"),
            "dns_name": load_balancer.get("DNSName"),
            "asset_type": "Load Balancer",
            "location": load_balancer.get("VpcId"),
            "vlan_network_id": load_balancer.get("VpcId"),
            "function": "Load Balancing",
            "comments": f"Scheme: {load_balancer.get('Scheme')}, State: {load_balancer.get('State', {}).get('Code')}"
        })
    return pd.DataFrame(records)
