from sources.dao import DAO
from sources.ctr.base_ctr import BaseCTR
from sources.ress.context_manager import transaction_scope

class DepartmentCTR(BaseCTR):
    def __init__(self):
        super().__init__("department")

    def add(self, name):
        with transaction_scope() as session:
            dao = DAO(session)
            dao.departement.create(name=name)
