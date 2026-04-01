from sources.dao import DAO
from sources.ctr.base_ctr import BaseCTR
from sources.ress.exceptions import DatabaseError
from sources.dao.base_dao import SessionLocal
from sources.ress.exceptions import EpicEventsError


class EventCTR(BaseCTR):
    def __init__(self):
        super().__init__("event")

    def get_table_for_all_events(self):
        events = self.get_all()
        return self.get_table_headers(events)

    def get_table_attribute_egal(self, attribute, value):
        events = self.get_attribute_egal(attribute, value)
        return self.get_table_headers(events)

    def get_table_headers(self, events):
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
