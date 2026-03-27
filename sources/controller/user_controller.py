from sources.dao import DAO
from sources.exceptions import DatabaseError
from sources.dao.base_dao import SessionLocal
from sqlalchemy.exc import IntegrityError
from sources.controller.tool_controller import Validators
from sources.exceptions import EpicEventsError

def get_departments():
    with SessionLocal() as session:
        dao = DAO(session)
        return dao.departement.get_all()

def add(first_name, last_name, email, password, department_id):
    with SessionLocal() as session:
        try:
            Validators.string_len(first_name,"first_name",0, 50)
            Validators.string_len(first_name,"last_name",0, 50)
            Validators.email(email)
            Validators.valid_password(password)
            dao = DAO(session)
            dao.user.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                department_id=department_id,
                password=password
            )
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise DatabaseError("Email non autorisé ou déjà utilisé.")
        except Exception as e:
            raise e

def get_table_for_all_users():
    with SessionLocal() as session:
        dao = DAO(session)
        users = dao.user.get_all()
        if not users:
            raise DatabaseError("Aucun utilisateur trouvé.") 
        table_data = []
        for user in users:
            list = []
            list.append(user.id)
            list.append(user.first_name)
            list.append(user.last_name)
            list.append(user.email)
            list.append(user.department.name)
            table_data.append(list)

        headers = [
            "ID",
            "Prénom",
            "Nom",
            "Email",
            "Département",
        ]
        return headers, table_data

def exists(id_user):
    with SessionLocal() as session:
        dao = DAO(session)
        return dao.user.exists(id_user)
    
def get(id_user):
    with SessionLocal() as session:
        dao = DAO(session)
        return dao.user.get_by_id(id_user)

def get_department_name(id_user):
    with SessionLocal() as session:
        dao = DAO(session)
        user = dao.user.get_by_id(id_user)
        return user.department.name

def set_attribute(id_user, attribute, new_value):
    with SessionLocal() as session:
        dao = DAO(session)
        user = dao.user.get_by_id(id_user)
        setattr(user, attribute, new_value)
        try :
            match attribute:
                case "first_name" | "last_name":
                    Validators.valid_name(new_value)
                case "email":
                    Validators.email(new_value)
                case _:
                    pass
            session.commit()
        except EpicEventsError as e:
            session.rollback()
            raise e
        except Exception as e:
            session.rollback()
            raise DatabaseError("Enregistrement impossible.")

def delete(user):
    with SessionLocal() as session:
        dao = DAO(session)
        dao.user.delete(user)
        session.commit()