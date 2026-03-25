from sources.dao.base_dao import BaseDAO
from sources.models import User
from sqlalchemy import select

class UserDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session)
        self.model = User

    def get_by_mail(self, email):
        query = select(User).where(User.email == email)
        return self.session.execute(query).scalar_one_or_none()
    
    def create(self, **data):
        password = data.pop('password', None)
        new_user = self.model(**data)
        new_user.set_password(password)
        self.session.add(new_user)
        return new_user
