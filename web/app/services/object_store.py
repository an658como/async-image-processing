class ObjectStore:
    def __init__(self, client):
        self.client = client

    def bucket_names(self) -> list[str]:
        return {bucket["Name"] for bucket in self.client.list_buckets()["Buckets"]}

    def create_buckets(self, bucket_names: list[str]):
        for bucket_name in bucket_names:
            self.client.create_bucket(Bucket=bucket_name)
