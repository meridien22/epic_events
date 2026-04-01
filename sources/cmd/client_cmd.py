import click
from sources.ress.view import View
from sources.ress.token import Token
from sources.ress.exceptions import EpicEventsError, DatabaseError
from sources.ress.authorisation import login_required, permission_required, owns_client
from sources.ctr import ctr

@click.command()
@login_required
@permission_required("SELECT_CLIENT")
def list_client():
    """Lister les clients."""
    try:
        table = ctr.client.get_table_for_all_clients()
        View.display_table("Liste des clients", table[0], table[1])
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        View.display_error(f"[{error_type}] : {str(e)}")

@click.command()
@click.argument('first_name', type=click.STRING)
@click.argument('last_name', type=click.STRING)
@login_required
@permission_required("CREATE_CLIENT")
def add_client(first_name, last_name):
    """Ajouter un client."""
    email = View.display_prompt_string(f"Email du client")
    phone_number = View.display_prompt_string(f"Téléphone du client")
    try:
        choices = ctr.enterprise.get_dict_for_choices("name")
        enterprise_id = View.display_prompt_choices("Entreprises disponibles", choices)
        ctr.client.add(first_name, last_name, email, phone_number, enterprise_id)
        View.display_success(f"Client {first_name}  {last_name} créé.")
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        View.display_error(f"[{error_type}] : {str(e)}")

@click.command()
@click.argument('client_id', type=click.INT)
@login_required
@permission_required("UPDATE_MY_CLIENT")
@owns_client
def update_client(client_id):
    """Modifier un client."""
    # on vérifie que le client existe
    try:
        ctr.client.exists(client_id)
        client = ctr.client.get(client_id)
        View.display_info(f"Modification du client {client.first_name} {client.last_name}\n")
        # on demande quel est le champ à modifier
        choices_user = {
            '1': f"Prénom : {client.first_name}",
            '2': f"Nom : {client.last_name}",
            '3': f"Email : {client.email}",
            '4': f"Téléphone : {client.phone_number}",
            '5': f"Entreprise : {ctr.client.get_enterprise_name(client_id)}",
        }
        choices_db = {
            '1': 'first_name',
            '2': 'last_name',
            '3': 'email',
            '4': 'phone_number',
            '5': 'enterprise_id',
        }
        choice = View.display_prompt_choices("Champ à modifier", choices_user)
        attribute = choices_db[choice]
        match attribute:
            case "first_name" | "last_name" | "email" | "phone_number":
                new_value = View.display_prompt_string(f"Nouvelle valeur pour {attribute}")
            case "enterprise_id":
                choices = ctr.enterprise.get_dict_for_choices("name")
                new_value = View.display_prompt_choices("Entreprises disponibles", choices)
        ctr.client.set_attribute(client_id, attribute, new_value)
        View.display_success(f"Champ {attribute} modifié.")
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        View.display_error(f"[{error_type}] : {str(e)}")

