import typing as t

import boto3
import botocore

from ..settings import CloudProviders
from ..settings import ObjectStore as ObjectStoreSettings


class ObjectStore(t.Protocol):
    def bucket_names(self) -> list[str]: ...

    def create_buckets(self, bucket_names: list[str]): ...

    def upload_file(self, bucket_name: str, data: bytes, key: str): ...


class S3ObjectStore:
    def __init__(self, client):
        self.client = client

    def bucket_names(self) -> list[str]:
        return {bucket["Name"] for bucket in self.client.list_buckets()["Buckets"]}

    def create_buckets(self, bucket_names: list[str]):
        for bucket_name in bucket_names:
            self.client.create_bucket(Bucket=bucket_name)

    def upload_file(self, bucket_name: str, data: bytes, key: str):
        self.client.put_object(Bucket=bucket_name, Key=key, Body=data)


def cloud_client(settings: ObjectStoreSettings) -> botocore.client.S3:
    client = boto3.client(
        "s3",
        aws_access_key_id=settings.admin_user,
        aws_secret_access_key=settings.admin_password,
        endpoint_url=settings.endpoint,
    )
    return client


def get_object_store(cloud_provider: CloudProviders) -> ObjectStore:
    # Currently only aws is supported
    return S3ObjectStore
