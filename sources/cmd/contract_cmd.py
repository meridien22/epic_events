import click
from sources.ress.view import View
from sources.ress.exceptions import EpicEventsError
from sources.ress.authorisation import login_required, permission_required, owns_contrat_or_permission
from sources.ctr import ctr


@click.command()
@login_required
@permission_required("SELECT_CONTRACT")
def list_contract():
    """Lister les contrats."""
    try:
        table = ctr.contract.get_table_for_all_contracts()
        View.display_table("Liste des contrats", table[0], table[1])
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        View.display_error(f"[{error_type}] : {str(e)}")

@click.command()
@click.argument('client_id', type=click.INT)
@click.argument(
    'amount', 
    type=click.FloatRange(min=0.01, clamp=False)
)
@login_required
@permission_required("CREATE_CONTRACT")
def add_contract(client_id, amount):
    """Créer un contrat"""
    try:
        ctr.contract.add(client_id, amount)
        View.display_success(f"Contrat créé.")
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        View.display_error(f"[{error_type}] : {str(e)}")

@click.command()
@click.argument('contract_id', type=click.INT)
@login_required
@owns_contrat_or_permission("UPDATE_CONTRACT")
def update_contract(contract_id):
    """Modifier un contrat"""
    try:
        ctr.contract.exists(contract_id)
        contract = ctr.contract.get(contract_id)
        View.display_info(f"Modification du contrat {contract_id}\n")
        # on demande quel est le champ à modifier
        choices_user = {
            '1': f"Montant total : {contract.total_amount}",
            '2': f"Montant restant : {contract.remaining_amount}",
            '3': f"Signature : {ctr.contract.get_signature_status(contract)}",

        }
        choices_db = {
            '1': 'total_amount',
            '2': 'remaining_amount',
            '3': 'is_signed',
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
                new_value = values_db[choice]
    
        ctr.contract.set_attribute(contract_id, attribute, new_value)
        View.display_success(f"Champ {attribute} modifié.")
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        View.display_error(f"[{error_type}] : {str(e)}")

@click.command()
@login_required
@permission_required("FILTER_CONTRACT")
def filter_contract():
    """Filtrer les contrats"""
    choices = {
        "1": "Contrats non signés",
        "2": "Contrats non payés",
    }
    choice = View.display_prompt_choices("Choix du filtre", values_user)
    try:
        match choice:
            case "1":
                table = ctr.contract.get_table_attribute_egal("is_signed", "False")
            case "2":
                table = ctr.contract.get_table_attribute_not_egal("remaining_amount", 0)
        View.display_table("Liste des contrats", table[0], table[1])
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        View.display_error(f"[{error_type}] : {str(e)}")