from sources.dao.base_dao import BaseDAO
from sources.ress.models import Client
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class ClientDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session)
        self.model = Client
