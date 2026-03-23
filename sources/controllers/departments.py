import click
from sources.database.postgres import SessionLocal
from sources.models import Department
from sources.views import UserView
from sqlalchemy.exc import IntegrityError
from sources.controllers.auth import login_required, permission_required

@click.command()
@click.argument('name')
@login_required
@permission_required("dzdze")
def add_department(name):
    """Ajouter un département."""
    with SessionLocal() as session:
        try:
            new_dept = Department(name=name)
            session.add(new_dept)
            session.commit()
            UserView.display_success(f"Département '{name}' créé.")
        except IntegrityError as e:
            session.rollback()
            UserView.display_error("Ce nom de département n'est pas autorisé ou déjà utilisé.")
        except Exception as e:
            session.rollback()
            UserView.display_error("Une erreur inattendue est survenue")
