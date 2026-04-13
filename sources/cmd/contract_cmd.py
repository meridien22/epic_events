import click
from sources.ress.view import View
from sources.ress.authorisation import login_required, permission_required, owns_contrat_or_permission
from sources.ctr import ctr
from sources.ress.context_manager import cmd_scope
import sentry_sdk


@click.command()
@login_required
@permission_required("SELECT_CONTRACT")
def list_contract():
    """List all contracts."""
    with cmd_scope():
        contracts = ctr.contract.get_contracts_with_commercial()
        table = ctr.contract.get_table_with_headers(contracts, commercial=True)
        View.display_table("Liste des contrats", table[0], table[1])


@click.command()
@click.argument('client_id', type=click.INT)
@click.argument(
    'amount',
    type=click.FloatRange(min=0.01, clamp=False)
)
@login_required
@permission_required("CREATE_CONTRACT")
def add_contract(client_id, amount):
    """Create a contract"""
    with cmd_scope():
        ctr.contract.add(client_id, amount)
        View.display_success("Contrat créé.")


@click.command()
@click.argument('contract_id', type=click.INT)
@login_required
@owns_contrat_or_permission("UPDATE_CONTRACT")
def update_contract(contract_id):
    """Modify a client"""
    with cmd_scope():
        ctr.contract.exists(contract_id)
        contract = ctr.contract.get(contract_id, 'client')
        View.display_info(f"Modification du contrat {contract_id}\n")
        # on demande quel est le champ à modifier
        choices_user = {
            '1': f"Montant total : {contract.total_amount}",
            '2': f"Montant restant : {contract.remaining_amount}",
            '3': f"Signature : {ctr.contract.get_signature_status(contract)}",
            '4': f"Client : {contract.client}",

        }
        choices_db = {
            '1': 'total_amount',
            '2': 'remaining_amount',
            '3': 'is_signed',
            '4': 'client_id',
        }
        choice = View.display_prompt_choices("Champ à modifier", choices_user)
        attribute = choices_db[choice]
        match attribute:
            case "total_amount" | "remaining_amount":
                new_value = View.display_prompt_string(f"Nouvelle valeur pour {attribute}")
            case "is_signed":
                values_user = {
                    "1": "Contrat signé",
                    "0": "Contrat non signé",
                }
                values_db = {
                    "1": True,
                    "0": False,
                }
                choice = View.display_prompt_choices("Etat signature", values_user)
                if values_db[choice]:
                    message = f"CONTRACT SIGNED : Nouveau contrat signé ({contract_id})"
                    sentry_sdk.capture_message(message, level="info")
                new_value = values_db[choice]
            case 'client_id':
                clients = ctr.client.get_clients_for_current_commercial()
                choices = ctr.contract.get_dict_for_choices_from_records(clients)
                new_value = View.display_prompt_choices('Choix du client', choices)
        ctr.contract.set_attribute_contract(contract_id, attribute, new_value)
        View.display_success(f"Champ {attribute} modifié.")


@click.command()
@login_required
@permission_required("FILTER_CONTRACT")
def filter_contract():
    """Filtered list of clients."""
    choices = {
        "1": "Contrats non signés",
        "2": "Contrats non payés",
    }
    choice = View.display_prompt_choices("Choix du filtre", choices)
    with cmd_scope():
        match choice:
            case "1":
                contracts = ctr.contract.get_attribute_egal("is_signed", "False", "client")
                table = ctr.contract.get_table_with_headers(contracts)
            case "2":
                contracts = ctr.contract.get_attribute_not_egal("remaining_amount", 0, "client")
                table = ctr.contract.get_table_with_headers(contracts)
        View.display_table("Liste des contrats", table[0], table[1])
