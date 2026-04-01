import click
from sources.ress.view import View
from sources.ress.exceptions import EpicEventsError, DatabaseError
from sources.ress.authorisation import login_required, permission_required
from sources.ctr import ctr

@click.command()
@login_required
@permission_required("SELECT_EVENT")
def list_event():
    """Lister les événements."""
    try:
        table = ctr.event.get_table_for_all_events()
        View.display_table("Liste des événements", table[0], table[1])
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        View.display_error(f"[{error_type}] : {str(e)}")

@click.command()
@login_required
@permission_required("FILTER_EVENT")
def filter_event():
    """Filtrer les événements."""
    choices = {
        "1": "Evénements sans support",
    }
    choice = View.display_prompt_choices("Choix du filtre", choices)
    try:
        match choice:
            case "1":
                table = ctr.event.get_table_attribute_egal("support_id", "NULL")
        View.display_table("Liste des contrats", table[0], table[1])
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        View.display_error(f"[{error_type}] : {str(e)}")

@click.command()
@click.argument('event_id', type=click.INT)
@login_required
@permission_required("ADD_SUPPORT_TO_EVENT")
def add_support(event_id):
    """Associer un support à l'événement."""
    # on vérifie que l'événement existe
    try:
        ctr.event.exists(event_id)
        departments = ctr.department.get_attribute_egal("name", "Support")
        department_id = departments[0].id
        users_support = ctr.user.get_attribute_egal("department_id", department_id)
        choices = ctr.event.get_dict_for_choices_from_records(users_support, "first_name", "last_name")
        choice = View.display_prompt_choices("Choix du support", choices)
        ctr.event.set_attribute(event_id, "support_id", choice)
        View.display_success("Support attribué à l'événement")
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        View.display_error(f"[{error_type}] : {str(e)}")

@click.command()
@click.argument('name', type=click.STRING)
@login_required
@permission_required("CREATE_EVENT_CONTRACT")
def add_event(name):
    """Créer un événement"""
    try:
        contracts = ctr.contract.get_contracts_for_current_commercial()
        if contracts is None:
            raise DatabaseError("Aucun contrat pour associer l'événement.")
        
        event_data = {"name": name}

        choices = ctr.contract.get_dict_for_choices("date_creation", "total_amount", "remaining_amount")
        event_data['contract_id'] = View.display_prompt_choices('Choix du contrat', choices)
   
        departments = ctr.department.get_attribute_egal("name", "Support")
        department_id = departments[0].id
        users_support = ctr.user.get_attribute_egal("department_id", department_id)
        choices = ctr.event.get_dict_for_choices_from_records(users_support, "first_name", "last_name")
        event_data['support_id'] = View.display_prompt_choices('Choix du support', choices)

        choices = ctr.location.get_dict_for_choices("street", "postal_code", "city", "country")
        event_data['location_id'] = View.display_prompt_choices("Choix de l'adresse", choices)

        choices = {"1": "Partie", "2": "Business meeting", "3": "Off-site event"}
        event_data['type_event'] = View.display_prompt_choices("Type d'événement", choices)

        event_data['date_debut'] = View.display_prompt_date("Date de début")

        event_data['date_fin'] = View.display_prompt_date("Date de fin")

        event_data['expected_audience'] = View.display_prompt_int("Audience attendue")

        event_data['note'] = View.display_prompt_note("Note")

        # add(name, type_event, date_debut, date_fin, expected_audience, note, contract_id, support_id, location_id)
        View.display_success(f"Contrat créé.")
    except EpicEventsError as e:
        error_type = e.__class__.__name__
        View.display_error(f"[{error_type}] : {str(e)}")
