from sources.dao.base_dao import SessionLocal
from sources.dao import DAO
from sources.ress.exceptions import DatabaseError
import click

class BaseCTR:
    def __init__(self, dao_name):
        self.dao_name = dao_name

    def get_all(self, *relationships):
        with SessionLocal() as session:
            dao = DAO(session)
            # On récupère de manière dynamique l'attribut de la classe DAO
            target_dao = getattr(dao, self.dao_name)
            records = target_dao.get_all(*relationships)
            if not records:
                raise DatabaseError(f"Aucun(e) {self.dao_name} trouvé(e).")
            return records
        
    def get(self, id, *relationships):
        with SessionLocal() as session:
            dao = DAO(session)
            # On récupère de manière dynamique l'attribut de la classe DAO
            target_dao = getattr(dao, self.dao_name)
            item = target_dao.get_by_id(id, *relationships)
            if item is None:
                raise DatabaseError(f"L'objet {self.dao_name} avec l'identifiant {id} n'existe pas.")
            return item
    
    def set_attribute(self, id, attribute, value):
        with SessionLocal() as session:
            dao = DAO(session)
            target_dao = getattr(dao, self.dao_name)
            try:
                item = target_dao.get_by_id(id)
                setattr(item, attribute, value)
                session.commit()
            except Exception as e:
                session.rollback()
                raise DatabaseError("Enregistrement impossible.")
    
    def exists(self, id):
        with SessionLocal() as session:
            dao = DAO(session)
            target_dao = getattr(dao, self.dao_name)
            if not target_dao.exists(id):
                raise DatabaseError(f"L'objet {self.dao_name} avec l'identifiant {id} n'existe pas.")
            
    def get_attribute_egal(self, attribute, value, *relationships):
        with SessionLocal() as session:
            dao = DAO(session)
            target_dao = getattr(dao, self.dao_name)
            records = target_dao.filter_by_attribute_egal(attribute, value, *relationships)
            if not records:
                raise DatabaseError(f"Aucun(e) {self.dao_name} trouvé(e).")
            return records
        
    def get_attribute_not_egal(self, attribute, value, *relationships):
        with SessionLocal() as session:
            dao = DAO(session)
            target_dao = getattr(dao, self.dao_name)
            records = target_dao.filter_by_attribute_not_egal(attribute, value, *relationships)
            if not records:
                raise DatabaseError(f"Aucun(e) {self.dao_name} trouvé(e).")
            return records

    def delete(self, id):
        with SessionLocal() as session:
            dao = DAO(session)
            target_dao = getattr(dao, self.dao_name)
            item = target_dao.get_by_id(id)
            target_dao.delete(item)
            session.commit()

    def get_dict_for_choices(self):
        with SessionLocal() as session:
            dao = DAO(session)
            target_dao = getattr(dao, self.dao_name)
            records = target_dao.get_all()
            return self.get_dict_for_choices_from_records(records)
    
    def get_dict_for_choices_from_records(self, records):
            return {record.id: str(record) for record in records}
