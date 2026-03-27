import click
from sources.controller.authorisation_controller import login_required, permission_required
from sources.command.tool_command import UserView
from sources.controller.contract_controller import (
    get_table_for_all_contracts,
    add,
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