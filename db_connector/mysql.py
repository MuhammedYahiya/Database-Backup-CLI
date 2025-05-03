import pymysql
import subprocess
import os
from cloud_storage import upload_to_gcs,upload_to_s3, download_from_s3,download_from_gcs
from utils import compress_file
import zipfile
from InquirerPy import inquirer
import tempfile

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
    

    
def backup_mysql(host, port, user, password, database, output_file, backup_dir='backups/mysql', upload_to_cloud=False, bucket_name=None, keep_local=True, upload_to_s3_enabled=False):
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
            
        print(f"Database dumped successfully to {output_sql_path}")
            
        compressed_path = compress_file(output_sql_path, compressed_backup_path)
        
        if not compressed_path:
            print("Compression failed. Aborting backup process")
        
        print(f"Backup successful! saved to {output_sql_path}")
        
        if upload_to_cloud and bucket_name:
            success = upload_to_gcs(bucket_name, compressed_backup_path, f"backups/mysql/{output_file}.zip" )
            
            if not keep_local:
                os.remove(compressed_backup_path)
                
        if upload_to_s3_enabled and bucket_name:
            success = upload_to_s3(compressed_backup_path, f"backups/mysql/{output_file}.zip", bucket_name)
            
            if not keep_local:
                os.remove(compressed_backup_path)
            
                
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {e}")
        return False



def restore_mysql(source, bucket_name=None, backup_dir='backups/mysql'):
    if source == 'local':
        zip_files = [f for f in os.listdir(backup_dir) if f.endswith('.zip')]
        if not zip_files:
            print("No local backup files found.")
            return False
        selected_file = inquirer.select(message="Choose a local backup:", choices=zip_files).execute()
        zip_path = os.path.join(backup_dir, selected_file)

    elif source == 'gcs':
        zip_name = inquirer.text(message="Enter the GCS backup file name (e.g. backup.zip):").execute()
        zip_path = os.path.join(tempfile.gettempdir(), zip_name)
        success = download_from_gcs(bucket_name, f"backups/mysql/{zip_name}", zip_path)
        if not success:
            print("Failed to download backup from GCS.")
            return False

    elif source == 's3':
        zip_name = inquirer.text(message="Enter the S3 backup file name (e.g. backup.zip):").execute()
        zip_path = os.path.join(tempfile.gettempdir(), zip_name)
        success = download_from_s3(f"backups/mysql/{zip_name}", zip_path, bucket_name)
        if not success:
            print("Failed to download backup from S3.")
            return False

    else:
        print("Unsupported restore source.")
        return False

    extract_path = os.path.join(tempfile.gettempdir(), 'restore_temp')
    os.makedirs(extract_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    sql_files = [f for f in os.listdir(extract_path) if f.endswith('.sql')]
    if not sql_files:
        print("No SQL file found in archive.")
        return False

    sql_path = os.path.join(extract_path, sql_files[0])

    host = inquirer.text(message="Database Host:").execute()
    port = int(inquirer.text(message="Port:", default="3306").execute())
    user = inquirer.text(message="Username:").execute()
    password = inquirer.secret(message="Password:").execute()
    database = inquirer.text(message="Database Name:").execute()

    try:
        command = ['mysql', '-h', host, '-P', str(port), '-u', user, f'-p{password}', database]
        with open(sql_path, 'r') as sql_file:
            subprocess.run(command, stdin=sql_file, check=True)
        print(f"✅ Database restored successfully from {source.upper()} backup")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Restore failed: {e}")
        return False
    finally:
        if os.path.exists(sql_path):
            os.remove(sql_path)
        if os.path.exists(zip_path):
            os.remove(zip_path)
        if os.path.exists(extract_path):
            os.rmdir(extract_path)
