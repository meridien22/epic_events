from sqlalchemy import select, exists
from sqlalchemy.orm import joinedload


class BaseDAO:
    def __init__(self, session):
        self.session = session
        self.model = None

    def get_by_id(self, obj_id, *relationships):
        """
        Executes an SQL query to retrieve all records from the table.
        Loads any relationships that exist.
        """
        query = select(self.model)
        for rel_name in relationships:
            rel_attr = getattr(self.model, rel_name)
            query = query.options(joinedload(rel_attr))
        query = query.where(self.model.id == obj_id)
        return self.session.execute(query).scalar_one_or_none()

    def get_all(self, *relationships):
        """
        Executes an SQL query to retrieve an object from the model using its identifier.
        Loads any relationships that exist.
        """
        query = select(self.model)
        for rel_name in relationships:
            rel_attr = getattr(self.model, rel_name)
            query = query.options(joinedload(rel_attr))
        return self.session.execute(query).scalars().all()

    def filter_by_attribute_egal(self, attr_name, value, *relationships):
        """
        Executes a query to return objects from a model
        based on an equality relationship between an attribute and a value.
        """
        column = getattr(self.model, attr_name)
        query = select(self.model)
        for rel_name in relationships:
            rel_attr = getattr(self.model, rel_name)
            query = query.options(joinedload(rel_attr))
        match value:
            case "null" | "NULL" | "Null":
                query = query.where(column.is_(None))
            case _:
                query = query.where(column == value)
        return self.session.execute(query).scalars().all()

    def filter_by_attribute_not_egal(self, attr_name, value, *relationships):
        """
        Executes a query to return objects from a model
        based on an inequality relationship between an attribute and a value.
        """
        column = getattr(self.model, attr_name)
        query = select(self.model)
        for rel_name in relationships:
            rel_attr = getattr(self.model, rel_name)
            query = query.options(joinedload(rel_attr))
        match value:
            case "null" | "NULL" | "Null":
                query = query.where(column.isnot(None))
            case _:
                query = query.where(column != value)
        return self.session.execute(query).scalars().all()

    def delete(self, obj):
        """Removes an object from the model."""
        if obj:
            self.session.delete(obj)

    def create(self, **data):
        """Creates a new object from a dictionary and adds it to the database."""
        new_obj = self.model(**data)
        self.session.add(new_obj)
        return new_obj

    def exists(self, obj_id):
        """Tests if an object with a given identifier exists in the database."""
        query = select(exists().where(self.model.id == obj_id))
        result = self.session.execute(query).scalar()
        return result
