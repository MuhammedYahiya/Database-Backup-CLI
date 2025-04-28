import pymysql
import subprocess
import os
import zipfile
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

def connect_mysql(host, port, user, password, database):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        print("MySQL connection successful!")
        return connection
    except pymysql.MySQLError as e:
        print(f"MySQL connection Failed: {e}")
        return None
    
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
    
def backup_mysql(host, port, user, password, database, output_file, backup_dir='backups', upload_to_cloud=False, bucket_name=None, keep_local=True):
    """Backup MysQL database and save to a .sql file."""
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"Backup directory '{backup_dir}' created.")
    try:
        command = [
            'mysqldump',
            '-h',host,
            '-P', str(port),
            '-u', user,
            '-p' + password,
            database,
        ]
        
        output_sql_path = os.path.join(backup_dir,f"{output_file}.sql")
        compressed_backup_path = os.path.join(backup_dir,f"{output_file}.zip")
        
        with open(output_sql_path, 'w') as backup_file:
            subprocess.run(command, stdout=backup_file, stderr=subprocess.PIPE, check=True)
            
        with zipfile.ZipFile(compressed_backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(output_sql_path, os.path.basename(output_sql_path))
            
        os.remove(output_sql_path)
        
        print(f"Backup successful! saved to {output_sql_path}")
        
        if upload_to_cloud and bucket_name:
            success = upload_to_gcs(bucket_name, compressed_backup_path, f"backups/{output_file}.zip" )
            
            if not keep_local:
                os.remove(compressed_backup_path)
                
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {e}")
        return False
