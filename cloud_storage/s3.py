import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError
import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_S3_BUCKET= os.getenv("AWS_S3_BUCKET")

def upload_to_s3(file_path, object_name=None, bucket_name=AWS_S3_BUCKET):
    if object_name is None:
        object_name = os.path.basename(file_path)
        
    try:
        s3_client = boto3.client(
            's3', 
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION
        )
        
        s3_client.upload_file(file_path,bucket_name,object_name)
        print(f"Uploaded to S3 bucket '{bucket_name}' as '{object_name}'")
        return True
    except (BotoCoreError, NoCredentialsError) as e:
        print(f"Failed to upload to S3: {e}")
        return False