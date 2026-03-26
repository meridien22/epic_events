import click
from sources.models import Enterprise
from sources.controller.token_controller import login_required, permission_required
from sqlalchemy import select
from sources.dao.base_dao import SessionLocal
from sources.command.views import UserView
from sqlalchemy.exc import IntegrityError
from sources.dao import DAO

@click.command()
@click.argument('name', type=click.STRING)
@login_required
@permission_required("CREATE_ENTERPRISE")
def add_enterprise(name):
    """Ajouter une entreprise."""
    with SessionLocal() as session:
        try:
            dao = DAO(session)
            dao.enterprise.create(name=name)
            session.commit()
            UserView.display_success(f"Entreprise '{name}' créé.")
        except IntegrityError as e:
            session.rollback()
            UserView.display_error("Ce nom d'entreprise' n'est pas autorisé ou déjà utilisé.")
        except Exception as e:
            session.rollback()
            UserView.display_error("Une erreur inattendue est survenue")