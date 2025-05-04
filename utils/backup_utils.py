import os
import subprocess
from cloud_storage import upload_to_gcs, upload_to_s3
from .compression import compress_file

def create_backup_command(db_type, host, port, user, password, database, output_file):
    """Create the appropriate backup command based on database type."""
    if db_type == 'mysql':
        return [
            'mysqldump',
            '-h', host,
            '-P', str(port),
            '-u', user,
            '-p', 
            database
        ]
    return None

def handle_backup(db_type, host, port, user, password, database, output_file, backup_dir='backups', upload_to_cloud=False, bucket_name=None, keep_local=True, upload_to_s3_enabled=False):
    """Handle the backup logic for various databases."""
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)  
        print(f"Backup directory '{backup_dir}' created.")
    
    try:
        command = create_backup_command(db_type, host, port, user, password, database, output_file)
        
        if command is None:
            raise ValueError("Unsupported database type for backup.")
        
        output_backup_path = os.path.join(backup_dir, f"{output_file}.backup")
        compressed_backup_path = os.path.join(backup_dir, f"{output_file}.zip")
        
        with open(output_backup_path, 'w') as outfile:
            subprocess.run(command, stdout=outfile, check=True)  
        
        print(f"Database dumped successfully to {output_backup_path}")
        
        compressed_path = compress_file(output_backup_path, compressed_backup_path)
        
        if not compressed_path:
            raise Exception("Compression failed. Aborting backup process.")
        
        print(f"Backup compressed and saved to {compressed_backup_path}")
        
        if upload_to_cloud and bucket_name:
            success = upload_to_gcs(bucket_name, compressed_backup_path, f"backups/{db_type}/{output_file}.zip")
            if not keep_local:
                os.remove(compressed_backup_path)

        if upload_to_s3_enabled and bucket_name:
            success = upload_to_s3(compressed_backup_path, f"backups/{db_type}/{output_file}.zip", bucket_name)
            if not keep_local:
                os.remove(compressed_backup_path)
                
    except subprocess.CalledProcessError as e:
        print(f"❌ Backup failed for MySQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    return True
