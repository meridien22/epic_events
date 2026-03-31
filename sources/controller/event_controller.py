from sources.dao import DAO
from sources.exceptions import DatabaseError
from sources.dao.base_dao import SessionLocal
from sources.exceptions import EpicEventsError

def get_table_for_all_events():
    with SessionLocal() as session:
        dao = DAO(session)
        events = dao.event.get_all()
        if not events:
            raise DatabaseError("Aucun événement trouvé.")
        else:
            return get_table_headers(events)
        

def get_table_attribute_egal(attribute_name, value):
    with SessionLocal() as session:
        dao = DAO(session)
        events = dao.event.filter_by_attribute_egal(attribute_name, value)
        if not events:
            raise DatabaseError("Aucun événement trouvé.")
        else:
            return get_table_headers(events)

def get_table_headers(events):
    table_data = []
    for event in events:
        list = []
        list.append(event.id)
        list.append(event.name)
        list.append(event.type_event)
        list.append(event.date_start)
        list.append(event.date_end)
        list.append(event.expected_audience)
        list.append(event.note)
        list.append(event.contract_id)
        if event.support is not None:
            list.append(f"{event.support.first_name} {event.support.last_name}")
        else:
            list.append(f"Aucun support")
        street = event.location.street
        code = event.location.postal_code
        city = event.location.city
        country = event.location.country
        list.append(f"{street} {code} {city} {country}")
        table_data.append(list)

    headers = [
        "ID",
        "Nom",
        "Type",
        "Date de début",
        "Date de fin",
        "Audience",
        "Note",
        "Contrat",
        "Support",
        "Emplacement",
    ]
    return headers, table_data

def exists(id_event):
    with SessionLocal() as session:
        dao = DAO(session)
        return dao.contract.exists(id_event)
    
def set_attribute(event_id, attribute, new_value):
    with SessionLocal() as session:
        dao = DAO(session)
        event = dao.event.get_by_id(event_id)
        setattr(event, attribute, new_value)
        try :
            session.commit()
        except EpicEventsError as e:
            session.rollback()
            raise e
        except Exception as e:
            session.rollback()
            raise DatabaseError("Enregistrement impossible.")