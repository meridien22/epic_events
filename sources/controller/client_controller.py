from sources.dao import DAO
from sources.exceptions import DatabaseError, EpicEventsError
from sources.dao.base_dao import SessionLocal
from sources.controller.tool_controller import Validators
from sqlalchemy.exc import IntegrityError
from sources.controller.token_controller import current_session

def get_table_for_all_clients():
    with SessionLocal() as session:
        dao = DAO(session)
        clients = dao.client.get_all()
        if not clients:
            raise DatabaseError("Aucun client trouvé.")
        
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

def add(first_name, last_name, email, phone_number, enterprise_id):
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

def set_attribute(id_client, attribute, new_value):
    with SessionLocal() as session:
        dao = DAO(session)
        client = dao.client.get_by_id(id_client)
        setattr(client, attribute, new_value)
        try:
            match attribute:
                case "first_name" | "last_name":
                    Validators.valid_name(new_value)
                case "email":
                    Validators.email(new_value)
                case "phone_number":
                    Validators.valid_phone_number(new_value)
                case _:
                    pass
            session.commit()
        except EpicEventsError as e:
            session.rollback()
            raise e
        except Exception as e:
            session.rollback()
            raise DatabaseError("Enregistrement impossible.")

def exists(id_client):
    with SessionLocal() as session:
        dao = DAO(session)
        return dao.client.exists(id_client)
    
def get(id_client):
    with SessionLocal() as session:
        dao = DAO(session)
        return dao.client.get_by_id(id_client)
    
def get_enterprise_name(client_id):
    with SessionLocal() as session:
        dao = DAO(session)
        client = dao.client.get_by_id(client_id)
        return client.enterprise.name