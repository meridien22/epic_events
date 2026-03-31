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
from sources.controller.user_controller import get_dict_user_support
from sources.exceptions import EpicEventsError

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