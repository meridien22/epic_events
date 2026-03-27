from sources.dao.base_dao import BaseDAO
from sources.models import Contract


class ContractDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session)
        self.model = Contract

