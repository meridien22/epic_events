from sources.dao.base_dao import BaseDAO
from sources.models import Location


class LocationDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session)
        self.model = Location
