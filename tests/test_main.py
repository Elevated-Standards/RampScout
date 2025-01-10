import unittest
from src.main import load_column_mapping, main

class TestMain(unittest.TestCase):
    def test_load_column_mapping(self):
        """
        Test that the column mapping is loaded correctly from the JSON configuration.
        """
        config_path = "config/column_mapping.json"
        column_mapping = load_column_mapping(config_path)
        self.assertIsInstance(column_mapping, dict)
        self.assertIn("UNIQUE ASSET IDENTIFIER", column_mapping)

    def test_main_execution(self):
        """
        Test that the main function executes without errors.
        """
        try:
            main()
        except Exception as e:
            self.fail(f"Main function raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
