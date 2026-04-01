import click
from sources.ress.authorisation import login_required, permission_required
from sources.ress.view import View
from sources.ress.exceptions import EpicEventsError
from sources.ctr import ctr


@click.command()
@click.argument('name', type=click.STRING)
@login_required
@permission_required("CREATE_ENTERPRISE")
def add_enterprise(name):
    """Ajouter une entreprise."""
    try:
        ctr.enterprise.add(name)
        View.display_success(f"Entreprise '{name}' créé.")
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        View.display_error(f"[{error_type}] : {str(e)}")
