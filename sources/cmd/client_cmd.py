import click
from sources.ress.view import View
from sources.ress.authorisation import login_required, permission_required, owns_client
from sources.ctr import ctr
from sources.ress.context_manager import cmd_scope


@click.command()
@login_required
@permission_required("SELECT_CLIENT")
def list_client():
    """List of all clients."""
    with cmd_scope():
        clients = ctr.client.get_all("enterprise", "commercial")
        table = ctr.client.get_table_with_headers(clients)
        View.display_table("Liste des clients", table[0], table[1])


@click.command()
@click.argument('first_name', type=click.STRING)
@click.argument('last_name', type=click.STRING)
@login_required
@permission_required("CREATE_CLIENT")
def add_client(first_name, last_name):
    """Add a client."""
    email = View.display_prompt_string("Email du client")
    phone_number = View.display_prompt_string("Téléphone du client")
    with cmd_scope():
        choices = ctr.enterprise.get_dict_for_choices()
        enterprise_id = View.display_prompt_choices("Entreprises disponibles", choices)
        ctr.client.add(first_name, last_name, email, phone_number, enterprise_id)
        View.display_success(f"Client {first_name}  {last_name} créé.")


@click.command()
@click.argument('client_id', type=click.INT)
@login_required
@permission_required("UPDATE_MY_CLIENT")
@owns_client
def update_client(client_id):
    """Modify a client."""
    # on vérifie que le client existe
    with cmd_scope():
        ctr.client.exists(client_id)
        client = ctr.client.get(client_id)
        View.display_info(f"Modification du client {client.first_name} {client.last_name}")
        View.display_separation_line()
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
                choices = ctr.enterprise.get_dict_for_choices()
                new_value = View.display_prompt_choices("Entreprises disponibles", choices)
        ctr.client.set_attribute_client(client_id, attribute, new_value)
        View.display_success(f"Champ {attribute} modifié.")
