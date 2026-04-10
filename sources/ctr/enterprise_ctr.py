from sources.dao import DAO
from sources.ctr.base_ctr import BaseCTR
from sources.ress.validators import Validators
from sources.ress.context_manager import transaction_scope


class EnterpriseCTR(BaseCTR):
    def __init__(self):
        super().__init__("enterprise")

    def add(self, name):
        with transaction_scope() as session:
            Validators.string_len(name, "nom", 3, 50)
            dao = DAO(session)
            dao.enterprise.create(name=name)
