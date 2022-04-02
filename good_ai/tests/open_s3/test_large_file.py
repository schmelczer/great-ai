from pathlib import Path
import unittest
from unittest.mock import Mock, create_autospec, patch

import botocore.session

PATH = Path(__file__).parent.resolve()


from src.open_s3 import LargeFile

credentials = {
    "aws_region_name": "your_region_like_eu-west-2",
    "aws_access_key_id": "YOUR_ACCESS_KEY_ID",
    "aws_secret_access_key": "YOUR_VERY_SECRET_ACCESS_KEY",
    "large_files_bucket_name": "create_a_bucket_and_put_its_name_here",
    "other_key": 23,
    "endpoint_url": "this is optional, for backblaze, use this: https://s3.us-west-002.backblazeb2.com",
}


class TestLargeFile(unittest.TestCase):
    def test_uninitialized(self):
        self.assertRaises(ValueError, LargeFile, "test-file")

    def test_bad_file_modes(self):
        self.assertRaises(ValueError, LargeFile, "test-file", "w", version=3)
        self.assertRaises(ValueError, LargeFile, "test-file", "wb", version=3)
        self.assertRaises(ValueError, LargeFile, "test-file", "w+r")
        self.assertRaises(ValueError, LargeFile, "test-file", "test")

    @patch("botocore.session")
    def test_initialized_with_dict(self, session):
        session_mock = Mock()
        session.get_session = create_autospec(
            botocore.session.get_session, return_value=session_mock
        )

        s3 = Mock()
        s3.list_objects_v2 = Mock(
            return_value={
                "Contents": [
                    {
                        "Key": "test-file/0",
                        "Size": 30,
                    },
                    {
                        "Key": "test-file/1",
                        "Size": 300,
                    },
                    {
                        "Key": "test-file/2",
                        "Size": 187,
                    },
                ]
            }
        )

        session_mock.create_client = Mock(return_value=s3)

        LargeFile.configure_credentials(**credentials)
        lf = LargeFile("test-file")
        session_mock.set_credentials.assert_called_once_with(
            access_key=credentials["aws_access_key_id"],
            secret_key=credentials["aws_secret_access_key"],
        )
        session_mock.create_client.assert_called_once_with(
            "s3",
            region_name=credentials["aws_region_name"],
            endpoint_url=credentials["endpoint_url"],
        )

        s3.list_objects_v2.assert_called_once_with(
            Bucket=credentials["large_files_bucket_name"], Prefix="test-file"
        )

        self.assertEqual(lf._version, 2)
        self.assertEqual(lf._local_name, "test-file-2")
        self.assertEqual(lf._s3_name, "test-file/2")

    @patch("botocore.session")
    def test_initialized_with_file(self, session):
        session_mock = Mock()
        session.get_session = create_autospec(
            botocore.session.get_session, return_value=session_mock
        )

        s3 = Mock()
        s3.list_objects_v2 = Mock(
            return_value={
                "Contents": [
                    {
                        "Key": "test-file/0",
                        "Size": 30,
                    },
                    {
                        "Key": "test-file/1",
                        "Size": 300,
                    },
                    {
                        "Key": "test-file/2",
                        "Size": 187,
                    },
                ]
            }
        )

        session_mock.create_client = Mock(return_value=s3)

        LargeFile.configure_credentials_from_file(PATH / "../../example_secrets.ini")
        lf = LargeFile("test-file")

        session_mock.set_credentials.assert_called_once_with(
            access_key=credentials["aws_access_key_id"],
            secret_key=credentials["aws_secret_access_key"],
        )
        session_mock.create_client.assert_called_once_with(
            "s3",
            region_name=credentials["aws_region_name"],
            endpoint_url=credentials["endpoint_url"],
        )

        assert s3.list_objects_v2.called
        s3.list_objects_v2.assert_called_once_with(
            Bucket=credentials["large_files_bucket_name"], Prefix="test-file"
        )

        self.assertEqual(lf._version, 2)
        self.assertEqual(lf._local_name, "test-file-2")
        self.assertEqual(lf._s3_name, "test-file/2")
