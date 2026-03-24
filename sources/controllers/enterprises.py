import click
from sources.models import Enterprise
from sources.controllers.auth import login_required, permission_required
from sqlalchemy import select
from sources.database.postgres import SessionLocal
from sources.views import UserView
from sqlalchemy.exc import IntegrityError

@click.command()
@click.argument('name', type=click.STRING)
@login_required
@permission_required("CREATE_ENTERPRISE")
def add_enterprise(name):
    """Ajouter une entreprise."""
    with SessionLocal() as session:
        try:
            enterprise = Enterprise(name=name)
            session.add(enterprise)
            session.commit()
            UserView.display_success(f"Entreprise '{name}' créé.")
        except IntegrityError as e:
            session.rollback()
            UserView.display_error("Ce nom d'entreprise' n'est pas autorisé ou déjà utilisé.")
        except Exception as e:
            session.rollback()
            UserView.display_error("Une erreur inattendue est survenue")