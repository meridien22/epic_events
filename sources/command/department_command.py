import click
from sources.dao.base_dao import SessionLocal
from sources.command.views import UserView
from sqlalchemy.exc import IntegrityError
from sources.controller.token_controller import login_required, permission_required
from sources.dao import DAO
from exceptions import EpicEventsError
from sources.controller.department_controller import add_department

@click.command()
@click.argument('name', type=click.STRING)
@login_required
@permission_required("CREATE_DEPARTMENT")
def add_department(name):
    """Ajouter un département."""
    with SessionLocal() as session:
        try:
            add_department(name)
            UserView.display_success(f"Département '{name}' créé.")
        except EpicEventsError as e:
            error_type = e.__class__.__name__
            UserView.display_error(f"[{error_type}] : {str(e)}")
