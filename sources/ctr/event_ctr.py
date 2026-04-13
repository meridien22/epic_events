from sources.dao import DAO
from sources.ctr.base_ctr import BaseCTR
from sources.ress.exceptions import FormError
from sources.ress.validators import Validators
from sources.ress.token import current_session
from sources.ress.context_manager import view_scope, transaction_scope


class EventCTR(BaseCTR):
    def __init__(self):
        """Defines the name of the DAO associated with the model."""
        super().__init__("event")

    def get_table_with_headers(self, events):
        """Returns a tuple composed of the headers and rows of the table represented as a list."""
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
                list.append("Aucun support")
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

    def add(self, event_data):
        """Opens a session to add a new event."""
        for key, value in event_data.items():
            self.validate_attribute(key, value)
        with transaction_scope() as session:
            dao = DAO(session)
            dao.event.create(
                name=event_data["name"],
                contract_id=event_data["contract_id"],
                support_id=event_data["support_id"],
                location_id=event_data["location_id"],
                type_event=event_data["type_event"],
                date_start=event_data["date_start"],
                date_end=event_data["date_end"],
                expected_audience=event_data["expected_audience"],
                note=event_data["note"],
            )

    def get_events_for_current_commercial(self):
        """Returns to commercial events."""
        user_id = current_session.user_id
        with view_scope() as session:
            dao = DAO(session)
            events = dao.event.get_events_user(user_id)
            return events

    def get_type_event(self):
        """Returns event types."""
        return {
            "1": "Partie",
            "2": "Business meeting",
            "3": "Off-site event"
        }

    def set_attribute_event(self, event_id, attribute, value):
        """Validates a value for an attribute and updates it using the base method."""
        self.validate_attribute(attribute, value)
        self.set_attribute(event_id, attribute, value)

    def validate_attribute(self, attribute, value):
        """Validates the attribute value of the model."""
        try:
            match attribute:
                case "name":
                    Validators.string_len(value, "nom", 0, 50)
                case "expected_audience":
                    Validators.valid_number_positive(value, "audience")
        except FormError as e:
            raise e
