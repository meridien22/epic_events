import click
from sources.controller.authorisation_controller import login_required, permission_required
from sources.command.tool_command import UserView
from sources.controller.tool_controller import Tools
from sources.controller.event_controller import (
    get_table_for_all_events,
    get_table_attribute_egal,
    exists,
    set_attribute,
)
from sources.controller.contract_controller import (
    get_contracts_for_current_commercial,
    get_dict_from_contracts
)
from sources.controller.user_controller import get_dict_user_support
from sources.exceptions import EpicEventsError
from datetime import datetime
from sources.controller.location_controller import get_dict_location

@click.command()
@login_required
@permission_required("SELECT_EVENT")
def list_event():
    """Lister les événements."""
    try:
        table = get_table_for_all_events()
        UserView.display_table("Liste des événements", table[0], table[1])
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        UserView.display_error(f"[{error_type}] : {str(e)}")

@click.command()
@login_required
@permission_required("FILTER_EVENT")
def filter_event():
    """Filtrer les événements."""
    choices = {
        "1": "Evénements sans support",
    }
    choice = click.prompt(
        f"Choix du filtre :\n{Tools.get_choice_dict(choices)}\nVotre choix ",
        type=click.Choice(choices.keys()),
        show_choices=False
    )
    try:
        match choice:
            case "1":
                table = get_table_attribute_egal("support_id", "NULL")
        UserView.display_table("Liste des contrats", table[0], table[1])
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        UserView.display_error(f"[{error_type}] : {str(e)}")

@click.command()
@click.argument('event_id', type=click.INT)
@login_required
@permission_required("ADD_SUPPORT_TO_EVENT")
def add_support(event_id):
    """Associer un support à l'événement."""
    # on vérifie que l'événement existe
    if not exists(event_id):
        UserView.display_error(f"L'événement avec l'ID {event_id} n'existe pas.")
        raise click.Abort()
    try:
        choices = get_dict_user_support()
        choice = click.prompt(
            f"Choix du support :\n{Tools.get_choice_dict(choices)}\nVotre choix ",
            type=click.Choice(choices.keys()),
            show_choices=False
        )
        set_attribute(event_id, "support_id", choice)
        UserView.display_success("Support attribué à l'événement")
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        UserView.display_error(f"[{error_type}] : {str(e)}")

@click.command()
@click.argument('name', type=click.STRING)
@login_required
@permission_required("CREATE_EVENT_CONTRACT")
def add_event(name):
    """Créer un événement"""
    try:
        contracts = get_contracts_for_current_commercial()
        if contracts is None:
            UserView.display_error(f"Aucun contrat pour associer l'événement.")
            raise click.Abort()
        
        event_data = {"name": name}

        choices = get_dict_from_contracts(contracts)
        event_data['contract_id'] = UserView.display_prompt_choices('Choix du contrat', choices)
   
        choices = get_dict_user_support()
        event_data['support_id'] = UserView.display_prompt_choices('Choix du support', choices)

        choices = get_dict_location()
        event_data['location_id'] = UserView.display_prompt_choices("Choix de l'adresse", choices)

        choices = {"1": "Partie", "2": "Business meeting", "3": "Off-site event"}
        event_data['type_event'] = UserView.display_prompt_choices("Type d'événement", choices)

        event_data['date_debut'] = UserView.display_prompt_date("Date de début")

        event_data['date_fin'] = UserView.display_prompt_date("Date de fin")

        event_data['expected_audience'] = UserView.display_prompt_int("Audience attendue")

        event_data['note'] = UserView.display_prompt_note("Note")

        # add(name, type_event, date_debut, date_fin, expected_audience, note, contract_id, support_id, location_id)
        UserView.display_success(f"Contrat créé.")
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        UserView.display_error(f"[{error_type}] : {str(e)}")
