import click

@click.group()
def cli():
    """DB Backup Utility"""
    pass

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