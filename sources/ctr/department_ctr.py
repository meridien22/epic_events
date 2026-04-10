from sources.dao import DAO
from sources.ctr.base_ctr import BaseCTR
from sources.ress.context_manager import transaction_scope


class DepartmentCTR(BaseCTR):
    def __init__(self):
        """Defines the name of the DAO associated with the model."""
        super().__init__("department")

    def add(self, name):
        """Opens a session to add a new departement."""
        with transaction_scope() as session:
            dao = DAO(session)
            dao.departement.create(name=name)
