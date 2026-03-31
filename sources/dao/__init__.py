from .user_dao import UserDAO
from .department_dao import DepartmentDAO
from .event_dao import EventDAO
from .client_dao import ClientDAO
from .enterprise_dao import EnterpriseDAO
from .contract_dao import ContractDAO
from .location_dao import LocationDAO

class DAO:
    def __init__(self, session):
        self.session = session
        self.user = UserDAO(self.session)
        self.department = DepartmentDAO(self.session)
        self.event = EventDAO(self.session)
        self.client = ClientDAO(self.session)
        self.enterprise = EnterpriseDAO(self.session)
        self.contract = ContractDAO(self.session)
        self.location = LocationDAO(self.session)