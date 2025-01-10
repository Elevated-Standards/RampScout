import unittest
import pandas as pd
from processors.ec2_processor import process_ec2
from processors.rds_processor import process_rds
from processors.s3_processor import process_s3

class TestProcessors(unittest.TestCase):
    def test_process_ec2(self):
        """
        Test the EC2 processor with sample input data.
        """
        sample_data = [
            {
                "Instances": [
                    {
                        "InstanceId": "i-1234567890abcdef",
                        "PrivateIpAddress": "192.168.1.1",
                        "NetworkInterfaces": [{"MacAddress": "00:11:22:33:44:55"}],
                        "PrivateDnsName": "ip-192-168-1-1.ec2.internal",
                        "InstanceType": "t2.micro",
                        "Placement": {"AvailabilityZone": "us-west-1a"},
                        "VpcId": "vpc-123abc",
                        "Tags": [{"Key": "Function", "Value": "Web Server"}]
                    }
                ]
            }
        ]
        df = process_ec2(sample_data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1)
        self.assertIn("unique_id", df.columns)
        self.assertEqual(df.iloc[0]["unique_id"], "i-1234567890abcdef")

    def test_process_rds(self):
        """
        Test the RDS processor with sample input data.
        """
        sample_data = [
            {
                "DBInstanceIdentifier": "rds-instance-1",
                "Endpoint": {"Address": "rds-instance-1.db.amazonaws.com"},
                "DBInstanceClass": "db.t2.micro",
                "AvailabilityZone": "us-west-1a",
                "DBSubnetGroup": {"VpcId": "vpc-123abc"},
                "Engine": "mysql",
                "EngineVersion": "8.0",
                "PubliclyAccessible": True,
                "TagList": [{"Key": "Function", "Value": "Database"}]
            }
        ]
        df = process_rds(sample_data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1)
        self.assertIn("unique_id", df.columns)
        self.assertEqual(df.iloc[0]["unique_id"], "rds-instance-1")

    def test_process_s3(self):
        """
        Test the S3 processor with sample input data.
        """
        sample_data = [
            {"Name": "my-s3-bucket", "CreationDate": "2023-01-01T00:00:00Z"}
        ]
        df = process_s3(sample_data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1)
        self.assertIn("unique_id", df.columns)
        self.assertEqual(df.iloc[0]["unique_id"], "my-s3-bucket")

if __name__ == "__main__":
    unittest.main()
