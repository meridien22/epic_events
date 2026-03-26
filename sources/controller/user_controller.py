from sources.dao import DAO
from sources.exceptions import DatabaseError
from sources.dao.base_dao import SessionLocal
from sqlalchemy.exc import IntegrityError
from sources.controller.tool_controller import Validators

def get_departments():
    with SessionLocal() as session:
        dao = DAO(session)
        return dao.departement.get_all()

def add(first_name, last_name, email, password, department_id):
    with SessionLocal() as session:
        try:
            Validators.StringLen(first_name,"first_name",0, 50)
            Validators.StringLen(first_name,"last_name",0, 50)
            Validators.Email(email)
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
