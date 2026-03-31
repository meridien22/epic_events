from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from private.parameter import parameter
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, exists

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

    def get_by_id(self, obj_id):
            return self.session.get(self.model, obj_id)
    
    def get_all(self):
            query = select(self.model)
            return self.session.execute(query).scalars().all()
    
    def filter_by_attribute_egal(self, attr_name, value):
         column = getattr(self.model, attr_name)
         match value:
            case "null" | "NULL" | "Null":
                query = select(self.model).where(column.is_(None))
            case "not null" | "NOT NULL":
                query = select(self.model).where(column.isnot(None))
            case _:
                query = select(self.model).where(column == value)
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