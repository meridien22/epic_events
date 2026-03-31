import click
from sources.controller.tool_controller import Tools
from sources.controller.authorisation_controller import (
    login_required,
    permission_required,
    owns_contrat_or_permission,
)
from sources.command.tool_command import UserView
from sources.controller.contract_controller import (
    get_table_for_all_contracts,
    add,
    exists,
    get,
    set_attribute,
    get_signature_status,
    get_table_attribute_egal,
    get_table_attribute_not_egal,
)
from sources.exceptions import EpicEventsError

@click.command()
@login_required
@permission_required("SELECT_CONTRACT")
def list_contract():
    """Lister les contrats."""
    try:
        table = get_table_for_all_contracts()
        UserView.display_table("Liste des contrats", table[0], table[1])
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        UserView.display_error(f"[{error_type}] : {str(e)}")

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
        add(client_id, amount)
        UserView.display_success(f"Contrat créé.")
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        UserView.display_error(f"[{error_type}] : {str(e)}")

@click.command()
@click.argument('contract_id', type=click.INT)
@login_required
@owns_contrat_or_permission("UPDATE_CONTRACT")
def update_contract(contract_id):
    """Modifier un contrat"""
    # on vérifie que le contrat existe
    if not exists(contract_id):
        UserView.display_error(f"Le contrat avec l'ID {contract_id} n'existe pas.")
        raise click.Abort()
    
    contract = get(contract_id)
    # on demande quel est le champ à modifier
    fields = {
        "1": (f"Montant total : {contract.total_amount}", "total_amount"),
        "2": (f"Montant restant : {contract.remaining_amount}", "remaining_amount"),
        "3": (f"Signature : {get_signature_status(contract)}", "is_signed"),
    }

    click.echo(f"Modification du contrat {contract_id}\n")
    menu = Tools.get_choice_from_field_update(fields)
    choice = click.prompt(
        f"{menu}\n\nQuel champ souhaitez-vous modifier ? ",
        type=click.Choice(fields.keys()),
        show_choices=False
    )

    label, attribute = fields[choice]
    label = label.split(": ")[0]
    match attribute:
        case "total_amount" | "remaining_amount":
            new_value = click.prompt(f"Nouvelle valeur pour {label}")
        case "is_signed":
            choices = {
                "1": ("Signé", True),
                "0": ("Non signé", False)
            }
            choice = click.prompt(
                "Statut du contrat :\n1 - Contrat signé\n0 - Contrat non signé\nVotre choix ",
                type=click.Choice(choices.keys()),
                show_choices=False
            )
            new_value = choices[choice][1]
    try:
        set_attribute(contract_id, attribute, new_value)
        UserView.display_success(f"Champ {label} modifié.")
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        UserView.display_error(f"[{error_type}] : {str(e)}")

@click.command()
@login_required
@permission_required("FILTER_CONTRACT")
def filter_contract():
    """Filtrer les contrats"""
    choices = {
        "1": "Contrats non signés",
        "2": "Contrats non payés",
    }
    choice = click.prompt(
        f"Choix du filtre :\n{Tools.get_choice_dict(choices)}\nVotre choix ",
        type=click.Choice(choices.keys()),
        show_choices=False
    )
    try:
        match choice:
            case "1":
                table = get_table_attribute_egal("is_signed", "False")
            case "2":
                table = get_table_attribute_not_egal("remaining_amount", 0)
        UserView.display_table("Liste des contrats", table[0], table[1])
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        UserView.display_error(f"[{error_type}] : {str(e)}")