import click
from sources.ress.view import View
from sources.ress.token import Token
from sources.ress.authorisation import login_required, permission_required
from sources.ctr import ctr
from sources.ress.context_manager import cmd_scope
import sentry_sdk


@click.command()
@click.option('--email', prompt=True, hide_input=False, help="Email")
@click.option('--password', prompt=True, hide_input=True, help="Mot de passe")
def login(email, password):
    """Connect a user."""
    with cmd_scope():
        token = Token()
        token.generate_token_from_email_password(email, password)
        View.display_success("Connexion réussie.")


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
    """Add a user."""
    with cmd_scope():
        if not email:
            email = click.prompt("Email de l'utilisateur")
        if not password:
            password = click.prompt("Mot de passe", hide_input=True, confirmation_prompt=True)
        choices = ctr.department.get_dict_for_choices()
        department_id = View.display_prompt_choices("Départements disponibles", choices)
        ctr.user.add(first_name, last_name, email, password, department_id)
        message = f"USER CREATE : Nouvel utilisateur {first_name} {last_name} créé"
        sentry_sdk.capture_message(message, level="info")
        View.display_success(f"Utilisateur {first_name}  {last_name} créé.")


@click.command()
@login_required
@permission_required("SELECT_USER")
def list_user():
    """List all uers."""
    with cmd_scope():
        users = ctr.user.get_all("department")
        table = ctr.user.get_table_with_headers(users)
        View.display_table("Liste des utilisateurs", table[0], table[1])


@click.command()
@click.argument('user_id', type=click.INT)
@login_required
@permission_required("UPDATE_USER")
def update_user(user_id):
    """Modify a user."""
    with cmd_scope():
        ctr.user.exists(user_id)
        user = ctr.user.get(user_id)
        View.display_info(f"Modification de l'utilisateur {user.first_name} {user.last_name}\n")
        # on demande quel est le champ à modifier
        choices_user = {
            '1': f"Prénom : {user.first_name}",
            '2': f"Nom : {user.last_name}",
            '3': f"Email : {user.email}",
            '4': f"Département : {ctr.user.get_department_name(user_id)}"
        }
        choices_db = {
            '1': 'first_name',
            '2': 'last_name',
            '3': 'email',
            '4': 'department_id'
        }
        choice = View.display_prompt_choices("Champ à modifier", choices_user)
        attribute = choices_db[choice]
        match attribute:
            case "first_name" | "last_name" | "email":
                new_value = View.display_prompt_string(f"Nouvelle valeur pour {attribute}")
            case "department_id":
                choices = ctr.department.get_dict_for_choices()
                new_value = View.display_prompt_choices("Départements disponibles", choices)
        ctr.user.set_attribute_user(user_id, attribute, new_value)
        message = f"USER UPDATE : Utilisateur {user.first_name} {user.last_name} {user.email} modifié"
        sentry_sdk.capture_message(message, level="info")
        View.display_success(f"Champ {attribute} modifié.")


@click.command()
@click.argument('user_id', type=click.INT)
@login_required
@permission_required("DELETE_USER")
def delete_user(user_id):
    """Delete a user."""
    # on vérifie que l'utilisateur existe
    with cmd_scope():
        ctr.user.exists(user_id)
        user = ctr.user.get(user_id)
        message = f"Êtes-vous sûr de vouloir supprimer {user.first_name} {user.last_name} ?"
        if click.confirm(message, default=False):
            ctr.user.delete(user_id)
            View.display_success("Utilisateur supprimé.")
        else:
            View.display_success("Supression annulé.")
