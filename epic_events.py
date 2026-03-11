from sources.models import User, Department
from sources.database import SessionLocal
from sources.setup_db import init_db

with SessionLocal() as session:

    # init_db()

    new_department = Department(name="Sales")
    session.add(new_department)

    department = session.query(Department).filter_by(name="Sales").first()

    new_user = User(first_name="Jean",
                    last_name="Dupont",
                    department=department,
                    email="jean@hotmail.com"
    )
    session.add(new_user)
    session.commit()
