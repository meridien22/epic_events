from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from private.parameter import parameter

# Database connection
user_db = parameter["user_db"]
password_db = parameter["password_db"]
name_db = parameter["name_db"]
engine = create_engine(
    f'postgresql+psycopg2://{user_db}:{password_db}@localhost:5432/{name_db}',
    echo=False
)

# Create a reusable configuration for a session.
SessionLocal = sessionmaker(bind=engine)
