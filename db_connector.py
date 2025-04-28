import pymysql
import subprocess

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
    
    
def backup_mysql(host, port, user, password, database, output_file):
    """Backup MysQL database and save to a .sql file."""
    try:
        command = [
            'mysqldump',
            '-h',host,
            '-P', str(port),
            '-u', user,
            '-p' + password,
            database,
        ]
        
        output_file_path = f"{output_file}.sql"
        
        with open(output_file_path, 'w') as backup_file:
            subprocess.run(command, stdout=backup_file, stderr=subprocess.PIPE, check=True)
            
        print(f"Backup successful! saved to {output_file_path}")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {e}")
        return False
