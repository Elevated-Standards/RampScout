import pandas as pd

def process_kms(data):
    """
    Process KMS JSON data and return a DataFrame.

    :param data: List of KMS keys from the JSON file.
    :return: A pandas DataFrame with KMS asset data.
    """
    records = []
    for key in data:
        records.append({
            "unique_id": key.get("KeyArn"),
            "asset_type": "KMS Key",
            "function": "Encryption",
            "comments": f"Key ID: {key.get('KeyId')}, Key State: {key.get('KeyState')}"
        })
    return pd.DataFrame(records)
