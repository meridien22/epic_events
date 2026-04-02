from sources.dao.base_dao import BaseDAO
from sources.ress.models import Event
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class EventDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session)
        self.model = Event

    def get_events_user(self, user_id):
        query = select(Event)
        rel_attr = getattr(self.model, "support")
        query = query.options(joinedload(rel_attr))
        rel_attr = getattr(self.model, "location")
        query = query.options(joinedload(rel_attr))
        query = query.where(Event.support_id == user_id)
        return self.session.execute(query).scalars().all()