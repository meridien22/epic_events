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
        # cette version de jointure fait un INNER JOIN (ramène que les contrats qui ont un client)
        query = (
            select(Contract)
            .join(Client,  self.model.client_id == Client.id)
            .options(joinedload(self.model.client))
            .where(Client.commercial_id == user_id)
            .where(~Contract.id.in_(subquery))
        )
        return self.session.execute(query).scalars().all()

    def get_contracts_with_commercial(self):
        """
        Retourne les contrats avec le nom du client et du commercial.
        """
        # cette version de jointure fait un LEFT JOIN (ramène tous les contrats même ceux qui n'ont pas de client)
        query = (
            select(Contract)
            .join(Contract.client)
            .join(Client.commercial)
            .options(
                joinedload(Contract.client).joinedload(Client.commercial)
            )
        )
        return self.session.execute(query).scalars().all()
