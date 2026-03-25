from sources.dao.base_dao import BaseDAO
from sources.models import User
from sqlalchemy import select

class UserDAO(BaseDAO):
    def get_by_mail(self, email):
        query = select(User).where(User.email == email)
        return self.session.execute(query).scalar_one_or_none()
    
    def get_by_id(self, user_id):
        return self.session.get(User, user_id)