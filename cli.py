import click
from db_connector import connect_mysql, backup_mysql
from dotenv import load_dotenv
import os
from InquirerPy import inquirer, get_style
from termcolor import colored


load_dotenv()

GOOGLE_CLOUD_BUCKET = os.getenv('GOOGLE_CLOUD_BUCKET')
AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET')

@click.group()
def cli():
    """DB Backup Utility"""
    pass

@cli.command()
@click.option('--host', prompt='Database Host', help='Host of the database')
@click.option('--port', prompt='Database Port', default=3306, help='Port of the database')
@click.option('--user', prompt='Username', help='Username for the database')
@click.option('--password', prompt='Password', help='Password for the database')
@click.option('--database', prompt='Database Name', help='Name of the database to connect')
def test_mysql_connection(host, port, user, password, database):
    """Test MySQL database connection."""
    connection = connect_mysql(host, port, user, password, database)
    if connection:
        click.echo("Connection successful")
    else:
        click.echo("Connection failed")
        
        
@cli.command()
@click.option('--host', prompt='Database Host', help='Host of the database')
@click.option('--port', prompt='Database Port', default=3306, help='Port of the database')
@click.option('--user', prompt='Username', help='Username for the database')
@click.option('--password', prompt='Password', help='Password for the database')
@click.option('--database', prompt='Database Name', help='Name of the database to connect')
@click.option('--output-file', prompt='Backup File Name (without extension)', help='Name of the output backup file')
def backup_mysql_command(host, port, user, password, database, output_file):
    """Backup MySQL database to a .sql file."""
    connection = connect_mysql(host, port, user, password, database)

    if connection:
        
        storage_options = [
            'Local Storage',
            'Google Cloud',
            'AWS S3',
            'Both Local and Google Cloud',
            'Both Local and AWS S3',
        ]
        
        custom_style = get_style({
            
            "pointer": "#00ff00 bold",  
            "questionmark": "#00ff00 bold",  
            "selected": "#00ff00 bold",  
        })
        
        selected_option = inquirer.select(
            message="Where do yo want to store the backup",
            choices=storage_options,
            pointer="➤",
            style=custom_style
        ).execute()
        
        if selected_option == 'Local Storage':
            success = backup_mysql(host, port, user, password, database, output_file)
            if success:
                click.echo(f"Backup saved successfully locally as {output_file}.zip")
        
        elif selected_option == 'Google Cloud':
            success = backup_mysql(host, port, user, password, database, output_file, upload_to_cloud=True, bucket_name=GOOGLE_CLOUD_BUCKET, keep_local=False)
            if success:
                click.echo(f"Backup uploaded successfully to Google Cloud Storage as {output_file}.zip")
                
        elif selected_option == "AWS S3":
            success = backup_mysql(host, port, user, password, database, output_file, upload_to_s3_enabled=True, bucket_name=AWS_S3_BUCKET, keep_local=False)
            if success:
                click.echo(f"Backup uploaded successfully to AWS S3 as {output_file}.zip")
                
        elif selected_option == 'Both Local and Google Cloud':
            success_local = backup_mysql(host, port, user, password, database, output_file)
            if success_local:
                click.echo(f"Backup saved successfully locally as {output_file}.zip")
                
            success_cloud = backup_mysql(host, port, user, password, database, output_file, upload_to_cloud=True, bucket_name=GOOGLE_CLOUD_BUCKET)
            if success_cloud:
                click.echo(f"Backup uploaded successfully to Google Cloud Storage as {output_file}.zip")
                
        elif selected_option == 'Both Local and AWS S3':
            success_local = backup_mysql(host, port, user, password, database, output_file)
            if success_local:
                click.echo(f"Backup saved successfully locally as {output_file}.zip")
                
            success = backup_mysql(host, port, user, password, database, output_file, upload_to_s3_enabled=True, bucket_name=AWS_S3_BUCKET)
            if success:
                click.echo(f"Backup uploaded successfully to AWS S3 as {output_file}.zip")
            
        
    else:
        click.echo("Could not connect to the database. Backup not performed")
        
@cli.command()
def backup():
    """Perform a backup"""
    click.echo("Backing up the database...")
    
    
@cli.command()
def restore():
    """Restore from a backup"""
    click.echo("Restoring the database...")
    

    
if __name__ == "__main__":
    cli()