from sources.ress.models import Base
from sources.ress.session import engine
from sources.ress.models import Department, Permission, User, Enterprise, Client, Contract, Location, Event
from sources.dao.base_dao import SessionLocal
from private.parameter import parameter
from sqlalchemy import select, text


def init_db():
    # Create all the tables in the database.
    Base.metadata.create_all(engine)

    # Inserts the data into the tables.
    with SessionLocal() as session:
        # Mise à zéro de la base de donnée
        tables = [
            "event",
            "contract",
            "client",
            "user",
            "department",
            "enterprise",
            "location",
            "departement_permission",
            "permission",
            "session"
        ]
        for table in tables:
            session.execute(text(f"TRUNCATE TABLE dev.{table} RESTART IDENTITY CASCADE;"))

        # Ajout des départements
        departments = ['Sales', 'Support', 'Management', 'Admin']
        for department in departments:
            dept = Department(name=department)
            session.add(dept)

        # Ajout des permissions génériques
        permissions = [
            "SELECT_CLIENT",
            "SELECT_CONTRACT",
            "SELECT_EVENT",
        ]
        for permission_name in permissions:
            permission = Permission(name=permission_name)
            for department in departments:
                department = session.query(Department).filter_by(name=department).first()
                department.permissions.append(permission)

        # Ajout des premissions par département
        department = session.query(Department).filter_by(name='Sales').first()
        permissions = [
            "CREATE_CLIENT",
            "UPDATE_MY_CLIENT",
            "UPDATE_CONTRACT",
            "FILTER_CONTRACT",
            "CREATE_EVENT_CONTRACT",
            "CREATE_ENTERPRISE",
        ]
        for permission_name in permissions:
            permission = Permission(name=permission_name)
            department.permissions.append(permission)

        department = session.query(Department).filter_by(name='Support').first()
        permissions = [
            "FILTER_EVENT",
            "UPDATE_MY_EVENT",
        ]
        for permission_name in permissions:
            permission = Permission(name=permission_name)
            department.permissions.append(permission)

        department = session.query(Department).filter_by(name='Management').first()
        permissions = [
            "SELECT_USER",
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
        permissions = [
            "CREATE_DEPARTMENT",
            "ADD_SUPPORT_TO_EVENT",
            "CREATE_CLIENT",
            "CREATE_CONTRACT",
            "CREATE_ENTERPRISE",
            "CREATE_EVENT_CONTRACT",
            "CREATE_USER",
            "DELETE_USER",
            "FILTER_CONTRACT",
            "FILTER_EVENT",
            "SELECT_CLIENT",
            "SELECT_CONTRACT",
            "SELECT_EVENT",
            "SELECT_USER",
            "UPDATE_CONTRACT",
            "UPDATE_MY_CLIENT",
            "UPDATE_MY_EVENT",
            "UPDATE_USER",
        ]
        for permission_name in permissions:
            permission = Permission(name=permission_name)
            department.permissions.append(permission)

        # Ajout des utilisateurs
        query = select(Department.id).where(Department.name == "Support")
        department_support_id = session.execute(query).scalar()
        query = select(Department.id).where(Department.name == "Sales")
        department_sales_id = session.execute(query).scalar()
        query = select(Department.id).where(Department.name == "Management")
        department_management_id = session.execute(query).scalar()
        query = select(Department.id).where(Department.name == "Admin")
        department_admin_id = session.execute(query).scalar()
        users = [
            ["Alain", "Support", "support1@proton.fr", department_support_id],
            ["Eric", "Support", "support2@proton.fr", department_support_id],
            ["Denis", "Sales", "sales1@proton.fr", department_sales_id],
            ["Valérie", "Sales", "sales2@proton.fr", department_sales_id],
            ["Sophie", "Management", "management@proton.fr", department_management_id],
            ["Véronique", "Admin", "admin@proton.fr", department_admin_id],
        ]
        for user_param in users:
            user = User(
                first_name=user_param[0],
                last_name=user_param[1],
                email=user_param[2],
                department_id=user_param[3],
            )
            match user_param[1]:
                case "Support":
                    user.set_password(parameter["password_support"]),
                case "Sales":
                    user.set_password(parameter["password_sales"]),
                case "Management":
                    user.set_password(parameter["password_management"]),
                case "Admin":
                    user.set_password(parameter["password_admin"]),
            session.add(user)

        # Ajout des entrerpises
        enterprises = ["Sobraga", "Setrag"]
        for entreprise_name in enterprises:
            enterprise = Enterprise(name=entreprise_name)
            session.add(enterprise)

        # Ajout des clients
        query = select(Enterprise.id).where(Enterprise.name == "Sobraga")
        enterprise_id = session.execute(query).scalar()
        query = select(User.id).where(User.email == "sales1@proton.fr")
        user_id = session.execute(query).scalar()
        clients = [
            ["Marcel", "Dupont", "marcel@sobraga.ga", "0489562358", enterprise_id, user_id],
            ["Albert", "Dupont", "albert@sobraga.ga", "0489562358", enterprise_id, user_id],
            ["Estelle", "Dupont", "estelle@sobraga.ga", "0489562358", enterprise_id, user_id],
            ["Amélie", "Dupont", "amelie@sobraga.ga", "0489562358", enterprise_id, user_id],
            ["Clémence", "Dupont", "clemence@sobraga.ga", "0489562358", enterprise_id, user_id],
            ["Erwan", "Dupont", "erwan@sobraga.ga", "0489562358", enterprise_id, user_id],
            ["Célestin", "Dupont", "celestin@sobraga.ga", "0489562358", enterprise_id, user_id],
        ]
        for client_param in clients:
            client = Client(
                first_name=client_param[0],
                last_name=client_param[1],
                email=client_param[2],
                phone_number=client_param[3],
                enterprise_id=client_param[4],
                commercial_id=client_param[5],
            )
            session.add(client)

        # Ajout des contrats
        query = select(Client.id).where(Client.first_name == "Marcel")
        client_id = session.execute(query).scalar()
        contracts = [
            [50000, 25000, 1, client_id],
            [0, 0, 0, client_id],
        ]
        for contratc_param in contracts:
            contract = Contract(
                total_amount=contratc_param[0],
                remaining_amount=contratc_param[1],
                is_signed=contratc_param[2],
                client_id=contratc_param[3],
            )
            session.add(contract)

        # Ajout des lieux
        locations = [
            ["rue Joseph Abonga", "1000", "Libreville", "Gabon"],
            ["rue Premier Campement", "2000", "Port-Gentil", "Gabon"],
            ["rue Agandja", "3000", "Franceville", "Gabon"],
            ["rue Batterie 4", "4000", "Makokou", "Gabon"],
        ]
        for location_param in locations:
            location = Location(
                street=location_param[0],
                postal_code=location_param[1],
                city=location_param[2],
                country=location_param[3],
            )
            session.add(location)

        # Ajout des événements
        query = select(Contract.id).where(Contract.total_amount == 50000)
        contract_id = session.execute(query).scalar()
        query = select(User.id).where(User.email == "support1@proton.fr")
        user_id = session.execute(query).scalar()
        query = select(Location.id).where(Location.city == "Franceville")
        location_id = session.execute(query).scalar()
        events = [
            ["Anniversaire de Gégé", "Partie", 2500, contract_id, user_id, location_id, "2026-06-21", "2026-06-22"],
        ]
        for event_param in events:
            event = Event(
                name=event_param[0],
                type_event=event_param[1],
                expected_audience=event_param[2],
                contract_id=event_param[3],
                support_id=event_param[4],
                location_id=event_param[5],
                date_start=event_param[6],
                date_end=event_param[7],
            )
            session.add(event)

        session.commit()
