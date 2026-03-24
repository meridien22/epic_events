from sources.database.setup_db import init_db
import click
from sources.controllers.departments import add_department
from sources.controllers.users import login
from sources.controllers.users import add_user
from sources.controllers.clients import list_client
from sources.controllers.enterprises import add_enterprise

init_db()

@click.group()
def cli():
    click.clear()
    click.echo(click.style("=== EPIC EVENTS CRM ===", fg="cyan", bold=True))
    click.echo("-" * 23)

cli.add_command(login)

cli.add_command(add_user)

cli.add_command(add_department)

cli.add_command(add_enterprise)

cli.add_command(list_client)

