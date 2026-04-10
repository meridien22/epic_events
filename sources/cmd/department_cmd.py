import click
from sources.ress.view import View
from sources.ress.authorisation import login_required, permission_required
from sources.ctr import ctr
from sources.ress.context_manager import cmd_scope


@click.command()
@click.argument('name', type=click.STRING)
@login_required
@permission_required("CREATE_DEPARTMENT")
def add_department(name):
    """Add a department."""
    with cmd_scope():
        ctr.department.add(name)
        View.display_success(f"Département '{name}' créé.")
