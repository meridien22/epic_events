from sources.dao.base_dao import BaseDAO
from sources.ress.models import Contract, Client
from sqlalchemy import select
from sqlalchemy.orm import joinedload

class ContractDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session)
        self.model = Contract

    def get_contracts_for_commercial(self, user_id):
        query = (
            select(self.model)
            .join(Client,  self.model.client_id == Client.id)
            .options(joinedload(self.model.client))
            .where(Client.commercial_id == user_id)
        )
        return self.session.execute(query).scalars().all()