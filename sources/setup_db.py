from sources.database import engine, Base
from sources.models import Department
from sources.database import SessionLocal

def init_db():
    Base.metadata.create_all(engine)
    departments=['Sales', 'Support', 'Management', 'Admin']
    with SessionLocal() as session:
        for department in departments:
            dept = Department(name=department)
            session.add(dept)
        session.commit()

if __name__ == "__main__":
    init_db()
