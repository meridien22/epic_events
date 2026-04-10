from .client_ctr import ClientCTR
from .contract_ctr import ContractCTR
from .department_ctr import DepartmentCTR
from .enterprise_ctr import EnterpriseCTR
from .event_ctr import EventCTR
from .location_ctr import LocationCTR
from .user_ctr import UserCTR


class CTR:
    """Container class for controller classes."""
    def __init__(self):
        self.client = ClientCTR()
        self.contract = ContractCTR()
        self.department = DepartmentCTR()
        self.enterprise = EnterpriseCTR()
        self.event = EventCTR()
        self.location = LocationCTR()
        self.user = UserCTR()


ctr = CTR()
