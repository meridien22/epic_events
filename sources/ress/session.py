from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from private.parameter import parameter

# Database connection
engine = create_engine(
    f'postgresql+psycopg2://epic_user:{parameter["password_db"]}@localhost:5432/epic_events',
    echo=False
)

# Create a reusable configuration for a session.
SessionLocal = sessionmaker(bind=engine)
