import click
from sources.validators import Validators
from sources.dao.base_dao import SessionLocal
from sources.models import User, Department
from sources.command.views import UserView
from sources.controller.token_controller import generate_token_from_email_password
from sources.dao import DAO
from exceptions import AuthError

@click.command()
@click.option('--email', prompt=True, hide_input=False, help="Email")
@click.option('--password', prompt=True, hide_input=True, help="Mot de passe")
def login(email, password):
    """Se connecter."""
    try:
        generate_token_from_email_password(email, password)
        UserView.display_success(f"Connexion réussie.")
    except AuthError as e:
        UserView.display_error(str(e))

@click.command()
@click.argument('first_name', type=click.STRING)
@click.argument('last_name', type=click.STRING)
@click.option('--email', prompt=True, help="Email de l'utilisateur")
@click.option(
    '--password', 
    prompt=True, 
    hide_input=True, 
    confirmation_prompt=True,
    help="Mot de passe sécurisé"
)
def add_user(first_name, last_name, email, password):
    """Ajouter un utilisateur."""
    Validators.StringLen(first_name,"first_name",0, 50)
    Validators.StringLen(first_name,"last_name",0, 50)
    Validators.email(email)
    
    with SessionLocal() as session:
        dao = DAO(session)
        departments = dao.departement.get_all()
        departments = {str(d.id): d.name for d in departments}
        menu_choice = "\n".join([f" [{k}] {v}" for k, v in departments.items()])
        department_id = click.prompt(
            f"Départements disponibles :\n{menu_choice}\nEntrez le code du département",
            type=click.Choice(list(departments.keys()))
        )

        try:
            dao = DAO(session)
            dao.user.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                department_id=department_id,
                password=password
            )
            session.add(new_user)
            session.commit()
            UserView.display_success(f"Utilisateur {first_name}  {last_name} créé.")
            
        except Exception as e:
            session.rollback()
            UserView.display_error("Impossible de créer cet utilisateur")