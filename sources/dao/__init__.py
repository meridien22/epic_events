from .user_dao import UserDAO
from .department_dao import DepartementDAO
from .event_dao import EventDAO
from .client_dao import ClientDAO
from .enterprise_dao import EnterpriseDAO
from .contract_dao import ContractDAO

class DAO:
    def __init__(self, session):
        self.session = session
        self.user = UserDAO(self.session)
        self.departement = DepartementDAO(self.session)
        self.event = EventDAO(self.session)
        self.client = ClientDAO(self.session)
        self.enterprise = EnterpriseDAO(self.session)
        self.contract = ContractDAO(self.session)