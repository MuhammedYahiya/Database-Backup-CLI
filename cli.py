import click
from db_connector import connect_mysql, backup_mysql

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
        success = backup_mysql(host, port, user, password, database, output_file)
        if success:
            click.echo(f"Backup saved successfully as {output_file}.sql")
        else:
            click.echo(f"Backup failed")
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