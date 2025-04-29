from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

def upload_to_gcs(bucket_name, source_file, destination_blob_name):
    """Upload a file to Google Cloud Storage"""
    try:
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file)
        
        print(f"Backup uploaded to Google Cloud Storage as {destination_blob_name}")
        return True
    
    except Exception as e:
        print(f"Google Cloud Storage upload failed: {e}")
        return False