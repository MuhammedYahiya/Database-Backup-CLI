
from utils import handle_backup, handle_restore

def backup_mysql(host, port, user, password, database, output_file, backup_dir='backups/mysql', upload_to_cloud=False, bucket_name=None, keep_local=True, upload_to_s3_enabled=False):
    """
    Backup MySQL database and save to a .sql file.
    """
    return handle_backup(
        db_type='mysql', 
        host=host, 
        port=port, 
        user=user, 
        password=password, 
        database=database, 
        output_file=output_file, 
        backup_dir=backup_dir, 
        upload_to_cloud=upload_to_cloud, 
        bucket_name=bucket_name, 
        keep_local=keep_local, 
        upload_to_s3_enabled=upload_to_s3_enabled
    )


def restore_mysql(source, bucket_name=None, backup_dir='backups/mysql'):
    """
    Restore MySQL database from a backup file.
    """
    return handle_restore(
        db_type='mysql',
        source=source,
        bucket_name=bucket_name,
        backup_dir=backup_dir
    )