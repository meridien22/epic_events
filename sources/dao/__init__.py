from .user_dao import UserDAO
from .department_dao import DepartementDAO

class DAO:
    def __init__(self, session):
        self.session = session
        self.user = UserDAO(self.session)
        self.departement = DepartementDAO(self.session)