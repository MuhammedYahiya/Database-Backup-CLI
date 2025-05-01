import click
import os
from dotenv import load_dotenv
from InquirerPy import inquirer, get_style
from db_connector import backup_mysql, connect_mysql

load_dotenv()

GOOGLE_CLOUD_BUCKET = os.getenv('GOOGLE_CLOUD_BUCKET')
AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET')

custom_style = get_style({
    "pointer": "#00ff00 bold",
    "questionmark": "#00ff00 bold",
    "selected": "#00ff00 bold",
})

@click.group()
def cli():
    """DB Backup Utility"""
    pass

@cli.command()
def backup():
    """Perform a backup for selected DB."""
    db_choices = {
        'MySQL': 'mysql',
        'PostgreSQL': 'postgresql',   # Placeholder
        'MongoDB': 'mongodb',         # Placeholder
        'SQLite': 'sqlite',           # Placeholder
    }

    selected_db = inquirer.select(
        message="Select the database to backup:",
        choices=list(db_choices.keys()),
        style=custom_style
    ).execute()

    if db_choices[selected_db] == 'mysql':
        host = click.prompt('Database Host')
        port = click.prompt('Database Port', default=3306)
        user = click.prompt('Username')
        password = click.prompt('Password', hide_input=True)
        database = click.prompt('Database Name')
        output_file = click.prompt('Backup File Name (without extension)')

        connection = connect_mysql(host, port, user, password, database)
        if not connection:
            click.echo("Could not connect to the database.")
            return

        storage_options = {
            'Local Storage': lambda: backup_mysql(host, port, user, password, database, output_file),
            'Google Cloud': lambda: backup_mysql(host, port, user, password, database, output_file, upload_to_cloud=True, bucket_name=GOOGLE_CLOUD_BUCKET, keep_local=False),
            'AWS S3': lambda: backup_mysql(host, port, user, password, database, output_file, upload_to_s3_enabled=True, bucket_name=AWS_S3_BUCKET, keep_local=False),
            'Both Local and Google Cloud': lambda: backup_mysql(host, port, user, password, database, output_file, upload_to_cloud=True, bucket_name=GOOGLE_CLOUD_BUCKET),
            'Both Local and AWS S3': lambda: backup_mysql(host, port, user, password, database, output_file, upload_to_s3_enabled=True, bucket_name=AWS_S3_BUCKET),
        }

        selected_storage = inquirer.select(
            message="Where do you want to store the backup?",
            choices=list(storage_options.keys()),
            style=custom_style
        ).execute()

        success = storage_options[selected_storage]()
        if success:
            click.echo(f"✅ Backup completed successfully to {selected_storage}")
        else:
            click.echo(f"❌ Backup failed for {selected_storage}")

    else:
        click.echo(f"{selected_db} support is coming soon!")

if __name__ == "__main__":
    cli()
