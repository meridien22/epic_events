from sources.dao.base_dao import BaseDAO
from sources.models import Client
from sqlalchemy import select


class ClientDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session)
        self.model = Client
