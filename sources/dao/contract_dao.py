from sources.dao.base_dao import BaseDAO
from sources.ress.models import Contract, Client, Event
from sqlalchemy import select
from sqlalchemy.orm import joinedload

class ContractDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session)
        self.model = Contract
    
    def get_unassigned_contracts_for_commercial(self, user_id):
        """
        Retourne les contrats qui n'ont pas encore d'événement associé.
        """
        subquery = select(Event.contract_id).scalar_subquery()
        query = (
            select(Contract)
            .join(Client,  self.model.client_id == Client.id)
            .options(joinedload(self.model.client))
            .where(Client.commercial_id == user_id)
            .where(~Contract.id.in_(subquery))
        )
        return self.session.execute(query).scalars().all()