import click
from sources.controller.authorisation_controller import login_required, permission_required
from sources.command.tool_command import UserView
from sources.exceptions import EpicEventsError
from sources.controller.enterprise_controller import add


@click.command()
@click.argument('name', type=click.STRING)
@login_required
@permission_required("CREATE_ENTERPRISE")
def add_enterprise(name):
    """Ajouter une entreprise."""
    try:
        add(name)
        UserView.display_success(f"Entreprise '{name}' créé.")
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        UserView.display_error(f"[{error_type}] : {str(e)}")
