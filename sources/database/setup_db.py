from sources.database.postgres import engine, Base
from sources.models import Department, Permission
from sources.database.postgres import SessionLocal

def init_db():
    Base.metadata.create_all(engine)
    departments=['Sales', 'Support', 'Management', 'Admin']
    with SessionLocal() as session:
        for department in departments:
            dept = Department(name=department)
            session.add(dept)

        permissions=[
            "SELECT_CLIENT",
            "SELECT_CONTRACT",
            "SELECT_EVENT",
        ]
        for permission_name in permissions:
            permission = Permission(name=permission_name)
            for department in departments:
                department = session.query(Department).filter_by(name=department).first()
                department.permissions.append(permission)

        department = session.query(Department).filter_by(name='Sales').first()
        permissions=[
            "CREATE_CLIENT",
            "UPDATE_MY_CLIENT",
            "UPDATE_MY_CLIENT_CONTRACT",
            "FILTER_CONTRACT",
            "CREATE_EVENT_CONTRACT",
        ]
        for permission_name in permissions:
            permission = Permission(name=permission_name)
            department.permissions.append(permission)

        department = session.query(Department).filter_by(name='Support').first()
        permissions=[
            "FILTER_EVENT",
            "UPDATE_MY_EVENT",
        ]
        for permission_name in permissions:
            permission = Permission(name=permission_name)
            department.permissions.append(permission)

        department = session.query(Department).filter_by(name='Management').first()
        permissions=[
            "CREATE_USER",
            "UPDATE_USER",
            "DELETE_USER",
            "CREATE_CONTRACT",
            "UPDATE_CONTRACT",
            "FILTER_EVENT",
            "ADD_SUPPORT_TO_EVENT",
        ]
        for permission_name in permissions:
            permission = Permission(name=permission_name)
            department.permissions.append(permission)

        department = session.query(Department).filter_by(name='Admin').first()
        permissions=[
        ]
        for permission_name in permissions:
            permission = Permission(name=permission_name)
            department.permissions.append(permission)
        
        session.commit()

if __name__ == "__main__":
    init_db()
