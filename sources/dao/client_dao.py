from sources.dao.base_dao import BaseDAO
from sources.ress.models import Client
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class ClientDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session)
        self.model = Client

    def get_clients_user(self, user_id):
        query = select(Client)
        rel_attr = getattr(self.model, "commercial")
        query = query.options(joinedload(rel_attr))
        query = query.where(Client.commercial_id == user_id)
        return self.session.execute(query).scalars().all()