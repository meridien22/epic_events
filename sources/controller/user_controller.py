import click
from sources.validators import Validators
from sources.dao.base_dao import SessionLocal
from sources.models import User, Department
from sources.view.views import UserView
from sources.controller.auth_controller import generate_token_from_email_password

@click.command()
@click.option('--email', prompt=True, hide_input=False, help="Email")
@click.option('--password', prompt=True, hide_input=True, help="Mot de passe")
def login(email, password):
    """Se connecter."""
    result = generate_token_from_email_password(email, password)
    if result == "Error":
        UserView.display_error("Email ou mot de passe incorrecte")
    else:
        UserView.display_success(f"Connexion réussie.")

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
        departments = session.query(Department).all()
        departments = {str(d.id): d.name for d in departments}
        menu_choice = "\n".join([f" [{k}] {v}" for k, v in departments.items()])
        department_id = click.prompt(
            f"Départements disponibles :\n{menu_choice}\nEntrez le code du département",
            type=click.Choice(list(departments.keys()))
        )

        try:
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                department_id=department_id
            )
            new_user.set_password(password)
            
            session.add(new_user)
            session.commit()
            UserView.display_success(f"Utilisateur {first_name}  {last_name} créé.")
            
        except Exception as e:
            session.rollback()
            UserView.display_error("Impossible de créer cet utilisateur")