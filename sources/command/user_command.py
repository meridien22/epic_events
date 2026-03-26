import click
from sources.controller.tool_controller import Tools
from sources.command.tool_command import UserView
from sources.controller.token_controller import Token
from sources.exceptions import EpicEventsError
from sources.controller.user_controller import get_departments, add
from sources.controller.authorisation_controller import login_required, permission_required

@click.command()
@click.option('--email', prompt=True, hide_input=False, help="Email")
@click.option('--password', prompt=True, hide_input=True, help="Mot de passe")
def login(email, password):
    """Se connecter."""
    try:
        token = Token()
        token.generate_token_from_email_password(email, password)
        UserView.display_success(f"Connexion réussie.")
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        UserView.display_error(f"[{error_type}] : {str(e)}")
        
@click.command()
@click.argument('first_name', type=click.STRING)
@click.argument('last_name', type=click.STRING)
@click.option('--email', help="Email de l'utilisateur")
@click.option(
    '--password', 
    hide_input=True, 
    help="Mot de passe sécurisé"
)
@login_required
@permission_required("CREATE_USER")
def add_user(first_name, last_name, email, password):
    """Ajouter un utilisateur."""
    try:
        if not email:
            email = click.prompt("Email de l'utilisateur")
        if not password:
            password = click.prompt("Mot de passe", hide_input=True, confirmation_prompt=True)
        departments = get_departments()
        param_choice = Tools.get_choice_from_id_name(departments)
        department_id = click.prompt(
            f"Départements disponibles :\n{param_choice[1]}\nEntrez le code du département",
            type=click.Choice(list(param_choice[0].keys()))
        )
        add(first_name, last_name, email, password, department_id)
        UserView.display_success(f"Utilisateur {first_name}  {last_name} créé.")
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        UserView.display_error(f"[{error_type}] : {str(e)}")