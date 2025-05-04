import os
import zipfile
import subprocess
import tempfile
from InquirerPy import inquirer
from cloud_storage import download_from_gcs, download_from_s3

def handle_restore(db_type, source, bucket_name=None, backup_dir='backups/mysql'):
    """Handle restoring backups for MySQL database only."""
    if db_type != 'mysql':
        print("❌ Only MySQL restore is supported currently.")
        return False

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

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        backup_files = [f for f in os.listdir(extract_path) if f.endswith('.backup')]
        if not backup_files:
            print("❌ No .backup file found in archive.")
            return False

        backup_path = os.path.join(extract_path, backup_files[0])

        host = inquirer.text(message="Database Host:").execute()
        port = int(inquirer.text(message="Port:", default="3306").execute())
        user = inquirer.text(message="Username:").execute()
        password = inquirer.secret(message="Password:").execute()
        database = inquirer.text(message="Database Name:").execute()

        command = ['mysql', '-h', host, '-P', str(port), '-u', user, f'-p{password}', database]

        with open(backup_path, 'r') as sql_file:
            subprocess.run(command, stdin=sql_file, check=True)

        print(f"✅ Database restored successfully from {source.upper()} backup")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Restore failed: {e}")
        return False

    finally:
        for file in [zip_path, backup_path]:
            if os.path.exists(file):
                os.remove(file)
        if os.path.exists(extract_path):
            os.rmdir(extract_path)
