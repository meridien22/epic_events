import click
from sources.command.tool_command import UserView
from sources.controller.authorisation_controller import login_required, permission_required
from sources.exceptions import EpicEventsError
from sources.controller.department_controller import add

@click.command()
@click.argument('name', type=click.STRING)
@login_required
@permission_required("CREATE_DEPARTMENT")
def add_department(name):
    """Ajouter un département."""
    try:
        add(name)
        UserView.display_success(f"Département '{name}' créé.")
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        UserView.display_error(f"[{error_type}] : {str(e)}")
