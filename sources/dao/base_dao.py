from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from private.parameter import parameter
from sqlalchemy.orm import DeclarativeBase

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