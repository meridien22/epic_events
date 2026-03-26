from sources.dao import DAO
from exceptions import DatabaseError
from sources.dao.base_dao import SessionLocal
from sqlalchemy.exc import IntegrityError

def add_departement(name):
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
