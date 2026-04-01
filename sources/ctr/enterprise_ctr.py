from sources.dao import DAO
from sources.ctr.base_ctr import BaseCTR
from sources.ress.exceptions import DatabaseError
from sources.dao.base_dao import SessionLocal
from sqlalchemy.exc import IntegrityError

class EnterpriseCTR(BaseCTR):
    def __init__(self):
        super().__init__("department")

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
