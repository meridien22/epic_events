from sources.dao import DAO
from sources.ctr.base_ctr import BaseCTR
from sources.ress.exceptions import DatabaseError, FormError
from sources.dao.base_dao import SessionLocal
from sqlalchemy.exc import IntegrityError
from sources.ress.validators import Validators

class EnterpriseCTR(BaseCTR):
    def __init__(self):
        super().__init__("enterprise")

    def add(self, name):
        with SessionLocal() as session:
            try:
                Validators.string_len(name,"nom",3, 50)
                dao = DAO(session)
                dao.enterprise.create(name=name)
                session.commit()
            except IntegrityError as e:
                session.rollback()
                raise DatabaseError("Entreprise non autorisé ou déjà utilisé.")
            except FormError as e:
                session.rollback()
                raise e
            except Exception as e:
                session.rollback()
                raise DatabaseError("Une erreur inattendue est survenue.")
