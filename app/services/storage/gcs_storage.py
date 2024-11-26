from google.cloud import storage
import json

class GCSStorage:
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def upload_json(self, file_name: str, data: dict):
        """Upload JSON data to GCS."""
        blob = self.bucket.blob(file_name)
        blob.upload_from_string(
            json.dumps(data),
            content_type="application/json"
        )
        print(f"Uploaded {file_name} to GCS bucket {self.bucket.name}.")

    def download_json(self, file_name: str) -> dict:
        """Download JSON data from GCS."""
        blob = self.bucket.blob(file_name)
        if blob.exists():
            return json.loads(blob.download_as_text())
        else:
            raise FileNotFoundError(f"File {file_name} not found in GCS bucket {self.bucket.name}.")
