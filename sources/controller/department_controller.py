from sources.dao import DAO
from sources.exceptions import DatabaseError
from sources.dao.base_dao import SessionLocal
from sqlalchemy.exc import IntegrityError

def get_departments():
    with SessionLocal() as session:
        dao = DAO(session)
        return dao.departement.get_all()

def add(name):
    with SessionLocal() as session:
        try:
            dao = DAO(session)
            dao.departement.create(name=name)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise DatabaseError("Département non autorisé ou déjà utilisé.")
        except Exception as e:
            session.rollback()
            raise DatabaseError("Une erreur inattendue est survenue.")
