from sources.dao import DAO
from sources.ress.exceptions import NotFoundError
from sources.ress.context_manager import view_scope, transaction_scope


class BaseCTR:
    """Parent class of all container classes."""
    def __init__(self, dao_name):
        """Defines the name of the DAO associated with the model."""
        self.dao_name = dao_name

    def get_all(self, *relationships):
        """
        Open a session to retrieve all objects from a model.
        Loads any relationships that exist.
        Throws a NotFoundError exception if the model contains no objects.
        """
        with view_scope() as session:
            dao = DAO(session)
            # On récupère de manière dynamique l'attribut de la classe DAO
            target_dao = getattr(dao, self.dao_name)
            records = target_dao.get_all(*relationships)
            if not records:
                raise NotFoundError(f"Aucun(e) {self.dao_name} trouvé(e).")
            return records

    def get(self, id, *relationships):
        """
        Open a session to retrieve an object from the model using its identifier.
        Loads any relationships that exist.
        Throws a NotFoundError exception if object does not exist.
        """
        with view_scope() as session:
            dao = DAO(session)
            # On récupère de manière dynamique l'attribut de la classe DAO
            target_dao = getattr(dao, self.dao_name)
            item = target_dao.get_by_id(id, *relationships)
            if item is None:
                raise NotFoundError(f"L'objet {self.dao_name} avec l'identifiant {id} n'existe pas.")
            return item

    def set_attribute(self, id, attribute, value):
        """Opens a session to update a model attribute."""
        with transaction_scope() as session:
            dao = DAO(session)
            target_dao = getattr(dao, self.dao_name)
            item = target_dao.get_by_id(id)
            setattr(item, attribute, value)
            session.commit()

    def exists(self, id):
        """
        Opens a session to test for the existence of an object defined by its ID.
        Raises a NotFoundError exception if the object does not exist.
        """
        with view_scope() as session:
            dao = DAO(session)
            target_dao = getattr(dao, self.dao_name)
            if not target_dao.exists(id):
                raise NotFoundError(f"L'objet {self.dao_name} avec l'identifiant {id} n'existe pas.")

    def get_attribute_egal(self, attribute, value, *relationships):
        """
        Opens a session to retrieve objects from the model
        based on an equality relationship between an attribute and a value.
        Raises a NotFoundError exception if no object matches the search criteria.
        """
        with view_scope() as session:
            dao = DAO(session)
            target_dao = getattr(dao, self.dao_name)
            records = target_dao.filter_by_attribute_egal(attribute, value, *relationships)
            if not records:
                raise NotFoundError(f"Aucun(e) {self.dao_name} trouvé(e).")
            return records

    def get_attribute_not_egal(self, attribute, value, *relationships):
        """
        Opens a session to retrieve objects from the model
        based on an inequality relationship between an attribute and a value.
        Raises a NotFoundError exception if no object matches the search criteria.
        """
        with view_scope() as session:
            dao = DAO(session)
            target_dao = getattr(dao, self.dao_name)
            records = target_dao.filter_by_attribute_not_egal(attribute, value, *relationships)
            if not records:
                raise NotFoundError(f"Aucun(e) {self.dao_name} trouvé(e).")
            return records

    def delete(self, id):
        """Deletes an object from the model based on its id."""
        with transaction_scope() as session:
            dao = DAO(session)
            target_dao = getattr(dao, self.dao_name)
            item = target_dao.get_by_id(id)
            target_dao.delete(item)

    def get_dict_for_choices(self):
        """
        Provides a dictionary with the model identifier as the key
        and the informal representation of the object as the value.
        """
        with view_scope() as session:
            dao = DAO(session)
            target_dao = getattr(dao, self.dao_name)
            records = target_dao.get_all()
            return self.get_dict_for_choices_from_records(records)

    def get_dict_for_choices_from_records(self, records):
        """
        Provides a dictionary with the records identifier as the key
        and the informal representation of the object as the value.
        """
        return {record.id: str(record) for record in records}
