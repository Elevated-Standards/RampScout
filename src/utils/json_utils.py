# Utility functions for handling JSON data
import json

def load_json(file_path):
    """
    Load JSON data from a file.

    :param file_path: Path to the JSON file.
    :return: Parsed JSON data as a Python object.
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file {file_path}: {e}")
        return []


def load_column_mapping(file_path):
    """
    Load column mapping configuration from a JSON file.
    """
    with open(file_path, 'r') as f:
        return json.load(f)