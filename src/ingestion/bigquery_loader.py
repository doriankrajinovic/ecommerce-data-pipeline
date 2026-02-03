"""
BigQuery Loader - učitava Parquet datoteke u BigQuery. 
"""

from pathlib import Path 
from google.cloud import bigquery  


def create_bigquery_client(credentials_path: Path): 
    """Kreira BigQuery klijent koristeći service account. 

    Args: 
        credentials_path: Putanja do credentials.json datoteke. 
    
    Returns: 
        BigQuery klijent objekt. """

    
    client= bigquery.Client.from_service_account_json(credentials_path)
    print(f"Connected to project: {client.project}")
    return client 



def create_dataset_if_not_exists(client, dataset_id):
    """Kreira dataset ako ne postoji.
     Args:
        client: BigQuery client
        dataset_id: Ime dataseta (npr. "ecommerce_raw")
    """

    full_dataset_id = f"{client.project}.{dataset_id}" 


    try: 
        client.get_dataset(full_dataset_id)
        print(f"Dataset {dataset_id} već postoji")
    except Exception: 
        #dataset ne postoji, kreiraj ga 
        dataset = bigquery.Dataset(full_dataset_id)
        dataset.location = "EU"
        client.create_dataset(dataset)
        


def load_parquet_to_bigquery(client, parquet_path, dataset_id, table_name): 
    """
    Učitava jednu Parquet datoteku u BigQuery tablicu.
    
    Args:
        client: BigQuery client
        parquet_path: Put do .parquet datoteke
        dataset_id: Ime dataseta
        table_name: Ime tablice
    """
    table_id = f"{client.project}.{dataset_id}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )


    print(f"Loading {parquet_path} to {table_id}...")
    
    with open(parquet_path, "rb") as file:
        job = client.load_table_from_file(file, table_id, job_config=job_config)
    
    # Čekaj da job završi
    job.result()
    
    # Provjeri broj redaka
    table = client.get_table(table_id)
    print(f"  Loaded {table.num_rows} rows to {table_name}")



def load_all_tables(credentials_path, data_dir, dataset_id):
    """
    Učitava sve Parquet datoteke u BigQuery.
    
    Args:
        credentials_path: Put do credentials.json
        data_dir: Folder s Parquet datotekama
        dataset_id: Ime dataseta u BigQuery
    """
    # Kreiraj klijent
    client = create_bigquery_client(credentials_path)
    
    # Kreiraj dataset ako ne postoji
    create_dataset_if_not_exists(client, dataset_id)
    
    # Lista tablica za učitavanje
    tables = ["customers", "products", "orders", "order_items"]
    
    # Učitaj svaku tablicu
    for table_name in tables:
        parquet_path = Path(data_dir) / f"{table_name}.parquet"
        
        if parquet_path.exists():
            load_parquet_to_bigquery(client, parquet_path, dataset_id, table_name)
        else:
            print(f"Warning: {parquet_path} not found, skipping")
    
    print("\nAll tables loaded successfully!")


if __name__ == "__main__":
    # Pokreni upload
    load_all_tables(
        credentials_path="credentials.json",
        data_dir="data/raw",
        dataset_id="ecommerce_raw"
    )