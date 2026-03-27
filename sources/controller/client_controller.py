from sources.dao import DAO
from sources.exceptions import DatabaseError
from sources.dao.base_dao import SessionLocal

def get_table_for_all_clients():
    with SessionLocal() as session:
        dao = DAO(session)
        clients = dao.client.get_all()
        if not clients:
            raise DatabaseError("Aucun client trouvé.")
        
        table_data = []
        for client in clients:
            list = []
            list.append(client.id)
            list.append(client.first_name)
            list.append(client.last_name)
            list.append(client.email)
            list.append(client.phone_number)
            list.append(client.date_creation)
            list.append(client.date_update)
            list.append(client.enterprise.name)
            list.append(f"{client.commercial.first_name} {client.commercial.last_name}")
            table_data.append(list)

        headers = [
            "ID",
            "Prénom",
            "Nom",
            "Email",
            "Téléphone",
            "Date création",
            "Date mise à jour",
            "Entreprise",
            "Commercial"
        ]
        return headers, table_data
