import os
from werkzeug.datastructures import FileStorage
from dotenv import load_dotenv
from flask import current_app
from google.cloud import storage
from google.cloud import exceptions as gcs_exceptions



def build_image_url(animal_id, filename=None):
    bucket_name = os.environ.get('GCP_PUBLIC_BUCKET_NAME')
    base_url = current_app.config['GCP_BASE_URL']
    path = current_app.config['GCP_IMAGE_ASSETS_PATH']
    if filename is None:
        return f"{base_url}/{bucket_name}/{path}/{animal_id}"
    else:
        return f"{base_url}/{bucket_name}/{path}/{animal_id}/{filename}"
    
def get_gcs_public_config():
    bucket_name = os.getenv('GCP_PUBLIC_BUCKET_NAME')
    assets_path = current_app.config['GCP_IMAGE_ASSETS_PATH']
    animal_image_limit = current_app.config['GCP_ANIMAL_IMAGE_LIMIT']
    config = {"bucket_name": bucket_name, "assets_path": assets_path, "animal_image_limit": animal_image_limit}
    return config
    
class GCSImageStorage:
    def __init__(self, bucket_name, path='assets/images/'):
        self.bucket_name = bucket_name
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(bucket_name)
        self.path = path
    
    def upload_animal_image_from_stream(self, file_obj: FileStorage, animal_id):
        """Uploads bytes from a stream or other file-like object to a blob."""
    
        # The stream or file (file-like object) from which to read
        # import io
        # file_obj = io.BytesIO()
        # file_obj.write(b"This is test data.")
        prefix = f"{self.path}{animal_id}"
        # The desired name of the uploaded GCS object (blob)
        destination_blob_name = f"{prefix}/{file_obj.filename}"
    
        blob = self.bucket.blob(destination_blob_name)

        # Rewind the stream to the beginning. This step can be omitted if the input
        # stream will always be at a correct position.
        file_obj.seek(0)

        # Upload data from the stream to your bucket.
        try:
            blob.upload_from_file(file_obj, content_type=file_obj.content_type)

            print(
                f"Stream data uploaded to {destination_blob_name} in bucket {self.bucket_name}."
            )
            return {"success": True, "filename": file_obj.filename}
        except gcs_exceptions.GoogleCloudError as e:
            return {"success": False, "error":str(e)}

    def list_animal_images(self, animal_id):
        prefix = f"{self.path}{animal_id}/"
        delimiter="/"
        filenames = []
        # Note: Client.list_blobs requires at least package version 1.17.0.
        blobs = self.storage_client.list_blobs(self.bucket_name, prefix=prefix, delimiter=delimiter)

        # # Note: The call returns a response only when the iterator is consumed.
        print("Blobs:")
        for blob in blobs:
            print(blob.name)
            filename = blob.name.split('/')[-1]
            if filename:
                filenames.append(filename)
            
        # if delimiter:
        #     print("Prefixes:")
        #     for prefix in blobs.prefixes:
        #         print(prefix)
                
        return filenames

