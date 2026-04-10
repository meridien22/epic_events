# from sources.ress.setup_db import init_db
import click
from sources.cmd.department_cmd import add_department
from sources.cmd.user_cmd import (
    login,
    add_user,
    list_user,
    update_user,
    delete_user,
)
from sources.cmd.client_cmd import (
    list_client,
    add_client,
    update_client,
)
from sources.cmd.enterprise_cmd import add_enterprise
from sources.cmd.contract_cmd import (
    list_contract,
    add_contract,
    update_contract,
    filter_contract,
)
from sources.cmd.event_cmd import (
    list_event,
    filter_event,
    add_support,
    add_event,
    update_event,
)
from sources.ress.authorisation import read_user_from_token
from sources.ress.view import View

# init_db()


@click.group()
def cli():
    click.clear()
    View.display_separation_line()
    View.display_epic_title()
    View.display_separation_line()
    View.display_parameter(read_user_from_token())
    View.display_separation_line()


cli.add_command(login)
cli.add_command(add_user)
cli.add_command(list_user)
cli.add_command(update_user)
cli.add_command(delete_user)

cli.add_command(add_department)

cli.add_command(add_enterprise)

cli.add_command(list_client)
cli.add_command(add_client)
cli.add_command(update_client)

cli.add_command(list_contract)
cli.add_command(add_contract)
cli.add_command(update_contract)
cli.add_command(filter_contract)

cli.add_command(list_event)
cli.add_command(filter_event)
cli.add_command(add_support)
cli.add_command(add_event)
cli.add_command(update_event)
