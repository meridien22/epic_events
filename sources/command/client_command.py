import click
from sources.controller.authorisation_controller import login_required, permission_required
from sources.command.tool_command import UserView
from sources.controller.client_controller import get_table_for_all_clients
from sources.exceptions import EpicEventsError

@click.command()
@login_required
@permission_required("SELECT_CLIENT")
def list_client():
    """Lister les clients."""
    try:
        table = get_table_for_all_clients()
        UserView.display_table("Liste des clients", table[0], table[1])
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        UserView.display_error(f"[{error_type}] : {str(e)}")

