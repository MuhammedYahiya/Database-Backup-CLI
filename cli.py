import click
from db_connector import connect_mysql

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
def backup():
    """Perform a backup"""
    click.echo("Backing up the database...")
    
    
@cli.command()
def restore():
    """Restore from a backup"""
    click.echo("Restoring the database...")
    

    
if __name__ == "__main__":
    cli()