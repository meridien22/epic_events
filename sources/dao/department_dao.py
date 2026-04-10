from sources.dao.base_dao import BaseDAO
from sources.ress.models import Department, Permission
from sqlalchemy import select


class DepartmentDAO(BaseDAO):
    def __init__(self, session):
        """Defines model and session."""
        super().__init__(session)
        self.model = Department

    def get_permission(self, departement_id):
        """Returns the permissions associated with a department."""
        query = (
            select(Permission.name)
            .join(Permission.departments)
            .where(Department.id == departement_id)
        )
        return self.session.execute(query).scalars().all()
