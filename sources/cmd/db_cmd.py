import click
from sources.ress.authorisation import login_required, permission_required
from sources.ress.context_manager import transaction_scope
from sources.ress.setup_db import init_db
from sources.ress.view import View

@click.command()
@login_required
@permission_required("CREATE_TABLE")
def create_table():
    """Create all tables for application."""
    try:
        init_db()
        View.display_success("Tables crées.")
    except Exception:
        View.display_error("Impossible de créer les tables.")