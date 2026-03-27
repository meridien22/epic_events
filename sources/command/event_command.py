import click
from sources.controller.authorisation_controller import login_required, permission_required
from sources.command.tool_command import UserView
from sources.controller.event_controller import get_table_for_all_events
from sources.exceptions import EpicEventsError

@click.command()
@login_required
@permission_required("SELECT_EVENT")
def list_event():
    """Lister les événements."""
    try:
        table = get_table_for_all_events()
        UserView.display_table("Liste des contrats", table[0], table[1])
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        UserView.display_error(f"[{error_type}] : {str(e)}")