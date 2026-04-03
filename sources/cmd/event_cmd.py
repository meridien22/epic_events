import click
from sources.ress.view import View
from sources.ress.exceptions import NotFoundError
from sources.ress.authorisation import login_required, permission_required, owns_event
from sources.ctr import ctr
from sources.ress.context_manager import cmd_scope

@click.command()
@login_required
@permission_required("SELECT_EVENT")
def list_event():
    """Lister les événements."""
    with cmd_scope():
        events = ctr.event.get_all("support", "location")
        table = ctr.event.get_table_with_headers(events)
        View.display_table("Liste des événements", table[0], table[1])

@click.command()
@login_required
@permission_required("FILTER_EVENT")
def filter_event():
    """Filtrer les événements."""
    choices = {
        "1": "Evénements sans support",
        "2": "Mes événements",
    }
    choice = View.display_prompt_choices("Choix du filtre", choices)
    with cmd_scope():
        match choice:
            case "1":
                events = ctr.event.get_attribute_egal("support_id", "NULL")
            case "2":
                events = ctr.event.get_events_for_current_commercial()
        table = ctr.event.get_table_with_headers(events)
        if not table[1]:
            View.display_info("Aucun événement à afficher")
        else:
            View.display_table("Liste des contrats", table[0], table[1])

@click.command()
@click.argument('event_id', type=click.INT)
@login_required
@permission_required("ADD_SUPPORT_TO_EVENT")
def add_support(event_id):
    """Associer un support à l'événement."""
    # on vérifie que l'événement existe
    with cmd_scope():
        ctr.event.exists(event_id)
        departments = ctr.department.get_attribute_egal("name", "Support")
        department_id = departments[0].id
        users_support = ctr.user.get_attribute_egal("department_id", department_id)
        choices = ctr.event.get_dict_for_choices_from_records(users_support)
        choice = View.display_prompt_choices("Choix du support", choices)
        ctr.event.set_attribute(event_id, "support_id", choice)
        View.display_success("Support attribué à l'événement")

@click.command()
@click.argument('name', type=click.STRING)
@login_required
@permission_required("CREATE_EVENT_CONTRACT")
def add_event(name):
    """Créer un événement"""
    with cmd_scope():
        contracts = ctr.contract.get_unassigned_contracts_for_current_commercial()
        if not contracts:
            raise NotFoundError("Aucun contrat pour associer l'événement.")
        
        event_data = {"name": name}

        choices = ctr.contract.get_dict_for_choices_from_records(contracts)
        event_data['contract_id'] = View.display_prompt_choices('Choix du contrat', choices)
   
        departments = ctr.department.get_attribute_egal("name", "Support")
        department_id = departments[0].id
        users_support = ctr.user.get_attribute_egal("department_id", department_id)
        choices = ctr.event.get_dict_for_choices_from_records(users_support)
        event_data['support_id'] = View.display_prompt_choices('Choix du support', choices)

        choices = ctr.location.get_dict_for_choices()
        event_data['location_id'] = View.display_prompt_choices("Choix de l'adresse", choices)

        choices = ctr.event.get_type_event()
        choice = View.display_prompt_choices("Type d'événement", choices)
        event_data['type_event'] = choices[choice]

        event_data['date_start'] = View.display_prompt_date("Date de début")

        event_data['date_end'] = View.display_prompt_date("Date de fin")

        event_data['expected_audience'] = View.display_prompt_int("Audience attendue")

        event_data['note'] = View.display_prompt_note("Note")

        ctr.event.add(event_data)
        View.display_success(f"Evénement créé.")

@click.command()
@click.argument('event_id', type=click.INT)
@login_required
@permission_required("UPDATE_MY_EVENT")
@owns_event
def update_event(event_id):
    """
    Modifier une événement
    """
    with cmd_scope():
        ctr.event.exists(event_id)
        event = ctr.event.get(event_id, "contract", "support", "location")
        View.display_info(f"Modification de l'événement {event.name} {event.date_start}")
        View.display_separation_line()
        # on demande quel est le champ à modifier
        choices_user = {
            '1': f"Name : {event.name}",
            '2': f"Type : {event.type_event}",
            '3': f"Date de début : {event.date_start}",
            '4': f"Date de fin : {event.date_end}",
            '5': f"Audience : {event.expected_audience}",
            '6': f"Note : {event.note}",
            '7': f"Contrat : {event.contract}",
            '8': f"Support : {event.support}",
            '9': f"Lieu : {event.location}",
        }
        choices_db = {
            '1': 'name',
            '2': 'type_event',
            '3': 'date_start',
            '4': 'date_end',
            '5': 'expected_audience',
            '6': 'note',
            '7': 'contract_id',
            '8': 'support_id',
            '9': 'location_id',
        }
        choice = View.display_prompt_choices("Champ à modifier", choices_user)
        attribute = choices_db[choice]
        match attribute:
            case 'name':
                new_value = View.display_prompt_string(f"Nouvelle valeur pour {attribute}")
            case 'type_event':
                choices = ctr.event.get_type_event()
                choice = View.display_prompt_choices("Type d'événement", choices)
                new_value = choices[choice]
            case 'date_start' | 'date_end':
                new_value = View.display_prompt_date("Nouvelle date")
            case 'expected_audience':
                new_value = View.display_prompt_int("Audience attendue")
            case 'note':
                new_value = View.display_prompt_note("Note")
            case 'contract_id':
                contracts = ctr.contract.get_unassigned_contracts_for_current_commercial()
                if not contracts:
                    raise NotFoundError("Aucun contrat pour associer l'événement.")
                choices = ctr.contract.get_dict_for_choices_from_records(contracts)
                new_value = View.display_prompt_choices('Choix du contrat', choices)
            case 'support_id':
                departments = ctr.department.get_attribute_egal("name", "Support")
                department_id = departments[0].id
                users_support = ctr.user.get_attribute_egal("department_id", department_id)
                choices = ctr.event.get_dict_for_choices_from_records(users_support)
                new_value = View.display_prompt_choices("Utilisateurs disponibles", choices)
            case 'location_id':
                choices = ctr.location.get_dict_for_choices()
                new_value = View.display_prompt_choices("Choix de l'adresse", choices)
        ctr.event.set_attribute_event(event_id, attribute, new_value)
        View.display_success(f"Champ {attribute} modifié.")
