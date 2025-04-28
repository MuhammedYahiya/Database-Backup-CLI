import pymysql
import subprocess
import os
import zipfile

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
    
    
def backup_mysql(host, port, user, password, database, output_file, backup_dir='backups'):
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
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {e}")
        return False
