from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from private.parameter import parameter
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, exists
from sqlalchemy.orm import joinedload

engine = create_engine(
    f'postgresql+psycopg2://epic_user:{parameter["password_db"]}@localhost:5432/epic_events',
    echo=False
)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    metadata = MetaData(schema="dev")


class BaseDAO:
    def __init__(self, session):
        self.session = session
        self.model = None

    def get_by_id(self, obj_id, *relationships):
        query = select(self.model)
        for rel_name in relationships:
            rel_attr = getattr(self.model, rel_name)
            query = query.options(joinedload(rel_attr))
        query = query.where(self.model.id == obj_id)
        return self.session.execute(query).scalar_one_or_none()

    def get_all(self, *relationships):
        query = select(self.model)
        for rel_name in relationships:
            rel_attr = getattr(self.model, rel_name)
            query = query.options(joinedload(rel_attr))
        return self.session.execute(query).scalars().all()

    def filter_by_attribute_egal(self, attr_name, value, *relationships):
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

    def save(self, obj):
        self.session.add(obj)
        return obj

    def delete(self, obj):
        if obj:
            self.session.delete(obj)

    def create(self, **data):
        new_obj = self.model(**data)
        self.session.add(new_obj)
        return new_obj

    def exists(self, obj_id):
        query = select(exists().where(self.model.id == obj_id))
        result = self.session.execute(query).scalar()
        return result
