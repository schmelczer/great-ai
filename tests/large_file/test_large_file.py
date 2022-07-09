from pathlib import Path
from typing import Any
from unittest.mock import Mock, patch

import boto3
import pytest

PATH = Path(__file__).parent.resolve()


from great_ai.large_file import LargeFileS3

credentials = {
    "aws_region_name": "your_region_like_eu-west-2",
    "aws_access_key_id": "YOUR_ACCESS_KEY_ID",
    "aws_secret_access_key": "YOUR_VERY_SECRET_ACCESS_KEY",
    "large_files_bucket_name": "create_a_bucket_and_put_its_name_here",
    "aws_endpoint_url": "this is optional, for backblaze, use this: https://s3.us-west-002.backblazeb2.com",
}


def test_uninitialized() -> None:
    with pytest.raises(ValueError):
        LargeFileS3("test-file")


def test_bad_file_modes() -> None:
    with pytest.raises(ValueError):
        LargeFileS3("test-file", "w", version=3)

    with pytest.raises(ValueError):
        LargeFileS3("test-file", "wb", version=3)

    with pytest.raises(ValueError):
        LargeFileS3("test-file", "w+r")

    with pytest.raises(ValueError):
        LargeFileS3("test-file", "test")


@patch.object(boto3, "client")
def test_initialized_with_dict(client: Any) -> None:
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
    boto3.client = Mock(return_value=s3)

    LargeFileS3.configure_credentials(
        aws_region_name=credentials["aws_region_name"],
        aws_access_key_id=credentials["aws_access_key_id"],
        aws_secret_access_key=credentials["aws_secret_access_key"],
        large_files_bucket_name=credentials["large_files_bucket_name"],
        aws_endpoint_url=credentials["aws_endpoint_url"],
    )
    lf = LargeFileS3("test-file")

    boto3.client.assert_called_once_with(
        "s3",
        aws_access_key_id=credentials["aws_access_key_id"],
        aws_secret_access_key=credentials["aws_secret_access_key"],
        region_name=credentials["aws_region_name"],
        endpoint_url=credentials["aws_endpoint_url"],
    )

    s3.list_objects_v2.assert_called_once_with(
        Bucket=credentials["large_files_bucket_name"], Prefix="test-file"
    )

    assert lf._version == 2
    assert lf._local_name == "test-file-2"


@patch.object(boto3, "client")
def test_initialized_with_file(client: Any) -> None:
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

    boto3.client = Mock(return_value=s3)

    LargeFileS3.configure_credentials_from_file(PATH / "data/example_secrets.ini")
    lf = LargeFileS3("test-file")

    boto3.client.assert_called_once_with(
        "s3",
        aws_access_key_id=credentials["aws_access_key_id"],
        aws_secret_access_key=credentials["aws_secret_access_key"],
        region_name=credentials["aws_region_name"],
        endpoint_url=credentials["aws_endpoint_url"],
    )

    assert s3.list_objects_v2.called
    s3.list_objects_v2.assert_called_once_with(
        Bucket=credentials["large_files_bucket_name"], Prefix="test-file"
    )

    assert lf._version == 2
    assert lf._local_name == "test-file-2"
