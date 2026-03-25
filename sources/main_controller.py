from sources.dao.setup_db import init_db
import click
from sources.controller.department_controller import add_department
from sources.controller.user_controller import login
from sources.controller.user_controller import add_user
from sources.controller.client_controller import list_client
from sources.controller.enterprise_controller import add_enterprise


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

