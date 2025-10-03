from google.cloud import storage
import os
import io
import config
import pandas as pd


def upload_to_gcs(file_path: str, bucket_name: str, destination_blob_name: str) -> None:
    """
    Uploads a file to Google Cloud Storage.

    Args:
        file_path (str): The local path to the file to upload.
        bucket_name (str): The name of the GCS bucket.
        destination_blob_name (str): The destination path in the GCS bucket.
    """
    # Autenticação usando o arquivo de credenciais
    storage_client = storage.Client.from_service_account_json(config.GCP_CREDENTIALS)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(file_path)

    print(f"File {file_path} uploaded to {destination_blob_name} in bucket {bucket_name}.") 
    
    
def get_information_from_gcs(bucket_name: str, blob_name: str) -> str:
    """
    Retrieves the content of a file stored in Google Cloud Storage.

    Args:
        bucket_name (str): The name of the GCS bucket.
        blob_name (str): The path to the file in the GCS bucket.

    Returns:
        str: The content of the file as a string.
    """
    # Autenticação usando o arquivo de credenciais
    storage_client = storage.Client.from_service_account_json(config.GCP_CREDENTIALS)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    content = blob.download_as_text()

    content_df = pd.read_csv(io.StringIO(content))
    return content_df

if __name__ == "__main__":
    for filename in os.listdir(config.DOWNLOAD_PATH):
        if filename.endswith(".mp4"):
            local_file_path = os.path.join(config.DOWNLOAD_PATH, filename)
            gcs_path = f"videos/{filename}"
            upload_to_gcs(local_file_path, config.GCP_BUCKET, gcs_path)
            print(f"Uploaded {filename} to GCS bucket {config.GCP_BUCKET} at {gcs_path}")

    # Example of retrieving information from GCS
    df = get_information_from_gcs(config.GCP_BUCKET, gcs_path)
    print(df.head())