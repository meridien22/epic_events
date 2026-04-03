import click
from sources.ress.authorisation import login_required, permission_required
from sources.ress.view import View
from sources.ctr import ctr
from sources.ress.context_manager import cmd_scope


@click.command()
@click.argument('name', type=click.STRING)
@login_required
@permission_required("CREATE_ENTERPRISE")
def add_enterprise(name):
    """Ajouter une entreprise."""
    with cmd_scope():
        ctr.enterprise.add(name)
        View.display_success(f"Entreprise '{name}' créé.")
