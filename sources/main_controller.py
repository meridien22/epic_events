from sources.dao.setup_db import init_db
import click
from sources.command.department_command import add_department
from sources.command.user_command import (
    login,
    add_user,
    list_user,
    update_user,
    delete_user,
)
from sources.command.client_command import list_client
from sources.command.enterprise_command import add_enterprise
from sources.command.contract_command import (
    list_contract,
    add_contract,
)
from sources.command.event_command import list_event


# init_db()

@click.group()
def cli():
    click.clear()
    click.echo(click.style("=== EPIC EVENTS CRM ===", fg="cyan", bold=True))
    click.echo("-" * 23)

cli.add_command(login)
cli.add_command(add_user)
cli.add_command(list_user)
cli.add_command(update_user)
cli.add_command(delete_user)

cli.add_command(add_department)

cli.add_command(add_enterprise)

cli.add_command(list_client)

cli.add_command(list_contract)
cli.add_command(add_contract)

cli.add_command(list_event)

