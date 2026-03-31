import click
from sources.controller.authorisation_controller import (
    login_required,
    permission_required,
    owns_client,
)
from sources.command.tool_command import UserView
from sources.controller.client_controller import (
    get_table_for_all_clients,
    add,
    set_attribute,
    exists,
    get,
    get_enterprise_name,
)
from sources.exceptions import EpicEventsError
from sources.controller.enterprise_controller import get_enterprises
from sources.controller.tool_controller import Tools

@click.command()
@login_required
@permission_required("SELECT_CLIENT")
def list_client():
    """Lister les clients."""
    try:
        table = get_table_for_all_clients()
        UserView.display_table("Liste des clients", table[0], table[1])
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        UserView.display_error(f"[{error_type}] : {str(e)}")

@click.command()
@click.argument('first_name', type=click.STRING)
@click.argument('last_name', type=click.STRING)
@login_required
@permission_required("CREATE_CLIENT")
def add_client(first_name, last_name):
    """Ajouter un client."""
    email = click.prompt("Email du client")
    phone_number = click.prompt("Téléphone du client")
    try:
        enterprises = get_enterprises()
        param_choice = Tools.get_choice_from_id_name(enterprises)
        enterprise_id = click.prompt(
            f"Entreprises disponibles :\n{param_choice[1]}\nEntrez le code de l'entreprise",
            type=click.Choice(list(param_choice[0].keys()))
        )
        add(first_name, last_name, email, phone_number, enterprise_id)
        UserView.display_success(f"Client {first_name}  {last_name} créé.")
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        UserView.display_error(f"[{error_type}] : {str(e)}")

@click.command()
@click.argument('client_id', type=click.INT)
@login_required
@permission_required("UPDATE_MY_CLIENT")
@owns_client
def update_client(client_id):
    """Modifier un client."""
    # on vérifie que le client existe
    if not exists(client_id):
        UserView.display_error(f"Le client avec l'ID {client_id} n'existe pas.")
        raise click.Abort()
    
    client = get(client_id)
    # on demande quel est le champ à modifier
    fields = {
        "1": (f"Prénom : {client.first_name}", "first_name"),
        "2": (f"Nom : {client.last_name}", "last_name"),
        "3": (f"Email : {client.email}", "email"),
        "4": (f"Téléphone : {client.phone_number}", "phone_number"),
        "5": (f"Entreprise : {get_enterprise_name(client_id)}", "enterprise_id")
    }

    click.echo(f"Modification du client {client.first_name} {client.last_name}\n")
    menu = Tools.get_choice_from_field_update(fields)
    choice = click.prompt(
        f"{menu}\n\nQuel champ souhaitez-vous modifier ? ",
        type=click.Choice(fields.keys()),
        show_choices=False
    )

    label, attribute = fields[choice]
    label = label.split(": ")[0]
    match attribute:
        case "first_name" | "last_name" | "email" | "phone_number":
            new_value = click.prompt(f"Nouvelle valeur pour {label}")
        case "enterprise_id":
            enterprises = get_enterprises()
            param_choice = Tools.get_choice_from_id_name(enterprises)
            enterprise_id = click.prompt(
                f"Entreprises disponibles :\n{param_choice[1]}\nEntrez le code de l'entreprise",
                type=click.Choice(list(param_choice[0].keys()))
            )
    try:
        set_attribute(client_id, attribute, new_value)
        UserView.display_success(f"Champ {label} modifié.")
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        UserView.display_error(f"[{error_type}] : {str(e)}")

