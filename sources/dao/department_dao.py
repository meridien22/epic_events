from sources.dao.base_dao import BaseDAO
from sources.ress.models import Department, Permission
from sqlalchemy import select


class DepartmentDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session)
        self.model = Department

    def get_permission(self, departement_id):
        query = (
            select(Permission.name)
            .join(Permission.departments)
            .where(Department.id == departement_id)
        )
        return self.session.execute(query).scalars().all()
