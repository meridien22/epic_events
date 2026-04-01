from sources.ctr.base_ctr import BaseCTR
from sources.dao import DAO
from sources.ress.exceptions import FormError, DatabaseError
from sources.dao.base_dao import SessionLocal
from sources.ress.validators import Validators
from sqlalchemy.exc import IntegrityError
from sources.ress.token import current_session


class ClientCTR(BaseCTR):
    def __init__(self):
        super().__init__("client")

    def get_table_for_all_clients(self):
        clients = self.get_all()
        
        table_data = []
        for client in clients:
            list = []
            list.append(client.id)
            list.append(client.first_name)
            list.append(client.last_name)
            list.append(client.email)
            list.append(client.phone_number)
            list.append(client.date_creation)
            list.append(client.date_update)
            list.append(client.enterprise.name)
            list.append(f"{client.commercial.first_name} {client.commercial.last_name}")
            table_data.append(list)

        headers = [
            "ID",
            "Prénom",
            "Nom",
            "Email",
            "Téléphone",
            "Date création",
            "Date mise à jour",
            "Entreprise",
            "Commercial"
        ]
        return headers, table_data

    def add(self, first_name, last_name, email, phone_number, enterprise_id):
        with SessionLocal() as session:
            try:
                Validators.valid_name(first_name,"first_name")
                Validators.valid_name(last_name,"last_name")
                Validators.email(email)
                Validators.valid_phone_number(phone_number)
                dao = DAO(session)
                dao.client.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    enterprise_id=enterprise_id,
                    commercial_id = current_session.user_id,
                )
                session.commit()
            except IntegrityError as e:
                session.rollback()
                raise DatabaseError("Email non autorisé ou déjà utilisé.")
            except Exception as e:
                raise e

    def set_attribute_client(self, id_client, attribute, value): 
        try:
            match attribute:
                case "first_name" | "last_name":
                    Validators.valid_name(value)
                case "email":
                    Validators.email(value)
                case "phone_number":
                    Validators.valid_phone_number(value)
            self.set_attribute(id_client, attribute, value)
        except FormError as e:
            raise e

    def get_enterprise_name(self, client_id):
        with SessionLocal() as session:
            dao = DAO(session)
            client = self.get_by_id(client_id)
            return client.enterprise.name