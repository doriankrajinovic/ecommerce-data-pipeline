from datetime import datetime 
from pathlib import Path 
from google.cloud import storage 

def create_gcs_client(credentials_path): 
    client = storage.Client.from_service_account_json(credentials_path)
    print(f"Connected to project: {client.project}")
    return client 

def upload_file_to_gcs(client, bucket_name, local_path, gcs_path): 
    bucket =client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)

    print(f"Uploading {local_path} to gs://{bucket_name}/{gcs_path}")
    blob.upload_from_filename(local_path)
    print(" Done!")


def upload_all_parquet_files(credentials_path, bucket_name, data_dir="data/raw"):
    client=create_gcs_client(credentials_path)
    today = datetime.now().strftime("%Y-%m-%d")

    files = ["customers.parquet", "products.parquet", "orders.parquet", "order_items.parquet"]

    print(f"Uploading files to gs://{bucket_name}/raw/{today}")
    print("-" * 50)

    for filename in files:
        local_path = Path(data_dir)/filename

        if local_path.exists():
            gcs_path = f"raw/{today}/{filename}"
            upload_file_to_gcs(client, bucket_name, str(local_path), gcs_path)
        else: 
            print(f"Warning: {local_path} not found, skipping")
    
    print("-" * 50)
    print(f"All files uploaded successfully to // {bucket_name}/raw/{today}")



if __name__ == "__main__":
    credentials_path = "credentials.json"
    bucket_name = "ecommerc-raw-dorian"
    upload_all_parquet_files(credentials_path, bucket_name)
