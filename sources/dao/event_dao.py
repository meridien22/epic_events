from sources.dao.base_dao import BaseDAO
from sources.ress.models import Event
from sqlalchemy import select


class EventDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session)
        self.model = Event
