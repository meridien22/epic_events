from sources.dao.base_dao import BaseDAO
from sources.ress.models import Enterprise


class EnterpriseDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session)
        self.model = Enterprise
