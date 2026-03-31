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
from sources.command.client_command import (
    list_client,
    add_client,
    update_client,
)
from sources.command.enterprise_command import add_enterprise
from sources.command.contract_command import (
    list_contract,
    add_contract,
    update_contract,
    filter_contract,
)
from sources.command.event_command import (
    list_event,
    filter_event,
    add_support,
    add_event,
)
from sources.controller.authorisation_controller import read_user_from_token
from sources.command.tool_command import UserView

# init_db()

@click.group()
def cli():
    click.clear()
    UserView.display_separation_line()
    UserView.display_epic_title()
    UserView.display_separation_line()
    UserView.display_parameter(read_user_from_token())
    UserView.display_separation_line()

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
cli.add_command(add_contract)
cli.add_command(filter_contract)

cli.add_command(update_contract)

cli.add_command(list_event)
cli.add_command(filter_event)
cli.add_command(add_support)
cli.add_command(add_event)

