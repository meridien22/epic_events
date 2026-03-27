import click
from sources.controller.tool_controller import Tools
from sources.command.tool_command import UserView
from sources.controller.token_controller import Token
from sources.exceptions import EpicEventsError
from sources.controller.user_controller import (
    get_departments,
    add,
    get_table_for_all_users,
    exists,
    get,
    get_department_name,
    set_attribute,
    delete
)
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
    except Exception as e:
        error_type = e.__class__.__name__
        UserView.display_error(f"[{error_type}] : {str(e)}")

@click.command()
@login_required
@permission_required("SELECT_USER")
def list_user():
    """Lister les utilisateurs."""
    try:
        table = get_table_for_all_users()
        UserView.display_table("Liste des utilisateurs", table[0], table[1])
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        UserView.display_error(f"[{error_type}] : {str(e)}")


@click.command()
@click.argument('user_id', type=click.INT)
@login_required
@permission_required("UPDATE_USER")
def update_user(user_id):
    """Modifier un utilisateur."""
    # on vérifie que l'utilisateur existe
    if not exists(user_id):
        UserView.display_error(f"L'utilisateur avec l'ID {user_id} n'existe pas.")
        raise click.Abort()

    user = get(user_id)
    # on demande quel est le champ à modifier
    fields = {
        "1": (f"Prénom : {user.first_name}", "first_name"),
        "2": (f"Nom : {user.last_name}", "last_name"),
        "3": (f"Email : {user.email}", "email"),
        "4": (f"Département : {get_department_name(user_id)}", "department_id")
    }

    click.echo(f"Modification de l'utilisateur {user.first_name} {user.last_name}\n")
    menu = Tools.get_choice_from_field_update(fields)
    choice = click.prompt(
        f"{menu}\n\nQuel champ souhaitez-vous modifier ? ",
        type=click.Choice(fields.keys()),
        show_choices=False
    )

    label, attribute = fields[choice]
    label = label.split(": ")[0]
    match attribute:
        case "first_name" | "last_name" | "email":
            new_value = click.prompt(f"Nouvelle valeur pour {label}")
        case "department_id":
            departments = get_departments()
            param_choice = Tools.get_choice_from_id_name(departments)
            new_value = click.prompt(
                f"Départements disponibles :\n{param_choice[1]}\nEntrez le code du département",
                type=click.Choice(list(param_choice[0].keys()))
            )
    try:
        set_attribute(user_id, attribute, new_value)
        UserView.display_success(f"Champ {label} modifié.")
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        UserView.display_error(f"[{error_type}] : {str(e)}")

@click.command()
@click.argument('user_id', type=click.INT)
@login_required
@permission_required("DELETE_USER")
def delete_user(user_id):
    """Supprimer un utilisateur."""
    # on vérifie que l'utilisateur existe
    if not exists(user_id):
        UserView.display_error(f"L'utilisateur avec l'ID {user_id} n'existe pas.")
        raise click.Abort()
    try:
        user = get(user_id)
        message = f"Êtes-vous sûr de vouloir supprimer {user.first_name} {user.last_name} ?"
        if click.confirm(message, default=False):
            delete(user)
            UserView.display_success(f"Utilisateur supprimé.")
        else:
            UserView.display_success(f"Supression annulé.")
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        UserView.display_error(f"[{error_type}] : {str(e)}")

