from sources.dao.base_dao import BaseDAO
from sources.models import Enterprise
from sqlalchemy import select


class EnterpriseDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session)
        self.model = Enterprise
