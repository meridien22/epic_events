import click
from sources.models import Client
from sources.controller.auth_controller import login_required, permission_required
from sqlalchemy import select
from sources.dao.base_dao import SessionLocal
from sources.view.views import UserView

@click.command()
@login_required
@permission_required("SELECT_CLIENT")
def list_client():
    """Lister les clients."""
    with SessionLocal() as session:
        query = select(Client)
        clients = session.execute(query).scalars().all()
        if not clients:
            UserView.display_info("Aucun client trouvé.")
            return

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

        headers = ["ID", "Prénom", "Nom", "Email", "Téléphone", "Date création", "Date mise à jour", "Entreprise", "Commercial"]

        UserView.display_table("Liste des clients", headers, table_data)
