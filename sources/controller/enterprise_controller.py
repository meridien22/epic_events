from sources.dao import DAO
from sources.exceptions import DatabaseError
from sources.dao.base_dao import SessionLocal
from sqlalchemy.exc import IntegrityError

def add(name):
    with SessionLocal() as session:
        try:
            dao = DAO(session)
            dao.enterprise.create(name=name)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise DatabaseError("Entreprise non autorisé ou déjà utilisé.")
        except Exception as e:
            session.rollback()
            raise DatabaseError("Une erreur inattendue est survenue.") 