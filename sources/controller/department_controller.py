import click
from sources.dao.base_dao import SessionLocal
from sources.models import Department
from sources.view.views import UserView
from sqlalchemy.exc import IntegrityError
from sources.controller.auth_controller import login_required, permission_required
from sources.dao import DAO

@click.command()
@click.argument('name', type=click.STRING)
@login_required
@permission_required("CREATE_DEPARTMENT")
def add_department(name):
    """Ajouter un département."""
    with SessionLocal() as session:
        try:
            dao = DAO(session)
            dao.departement.create(name=name)
            # controller debut
            session.commit()
            UserView.display_success(f"Département '{name}' créé.")
            # controller fin
        except IntegrityError as e:
            session.rollback()
            UserView.display_error("Ce nom de département n'est pas autorisé ou déjà utilisé.")
        except Exception as e:
            session.rollback()
            UserView.display_error("Une erreur inattendue est survenue")
