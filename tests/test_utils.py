import unittest
from utils.json_utils import load_json
from utils.excel_utils import write_to_excel
import os
import pandas as pd

class TestUtils(unittest.TestCase):
    def test_load_json_valid_file(self):
        """
        Test loading a valid JSON file.
        """
        sample_data = [{"key": "value"}]
        with open("sample.json", "w") as f:
            import json
            json.dump(sample_data, f)

        loaded_data = load_json("sample.json")
        self.assertEqual(loaded_data, sample_data)
        os.remove("sample.json")

    def test_load_json_invalid_file(self):
        """
        Test loading an invalid or non-existent JSON file.
        """
        loaded_data = load_json("nonexistent.json")
        self.assertEqual(loaded_data, [])

    def test_write_to_excel(self):
        """
        Test writing data to an Excel file.
        """
        # Prepare sample data
        data_frames = [
            pd.DataFrame({"unique_id": ["id1"], "ip_address": ["192.168.1.1"]}),
            pd.DataFrame({"unique_id": ["id2"], "ip_address": ["192.168.1.2"]})
        ]
        column_mapping = {"UNIQUE ASSET IDENTIFIER": "unique_id", "IPv4 or IPv6 Address": "ip_address"}
        template_path = "template.xlsx"
        output_dir = "test_output"

        # Create a mock template Excel file
        from openpyxl import Workbook
        wb = Workbook()
        wb.create_sheet(title="Inventory")
        wb.save(template_path)

        # Write data to the Excel file
        write_to_excel(template_path, data_frames, column_mapping, output_dir)

        # Verify output file existence
        output_files = os.listdir(output_dir)
        self.assertTrue(len(output_files) > 0)

        # Clean up
        os.remove(template_path)
        for file in output_files:
            os.remove(os.path.join(output_dir, file))
        os.rmdir(output_dir)

if __name__ == "__main__":
    unittest.main()
