from sources.dao import DAO
from sources.ress.exceptions import DatabaseError
from sources.dao.base_dao import SessionLocal
from sqlalchemy.exc import IntegrityError
from sources.ress.validators import Validators
from sources.ress.exceptions import FormError
from sources.ctr.base_ctr import BaseCTR


class UserCTR(BaseCTR):
    def __init__(self):
        super().__init__("user")

    def add(self, first_name, last_name, email, password, department_id):
        with SessionLocal() as session:
            try:
                Validators.string_len(first_name,"first_name",0, 50)
                Validators.string_len(first_name,"last_name",0, 50)
                Validators.email(email)
                Validators.valid_password(password)
                dao = DAO(session)
                dao.user.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    department_id=department_id,
                    password=password
                )
                session.commit()
            except IntegrityError as e:
                session.rollback()
                raise DatabaseError("Email non autorisé ou déjà utilisé.")
            except Exception as e:
                raise e

    def get_table_for_all_users(self):
        users = self.get_all()
        if not users:
            raise DatabaseError("Aucun utilisateur trouvé.") 
        table_data = []
        for user in users:
            list = []
            list.append(user.id)
            list.append(user.first_name)
            list.append(user.last_name)
            list.append(user.email)
            list.append(user.department.name)
            table_data.append(list)

        headers = [
            "ID",
            "Prénom",
            "Nom",
            "Email",
            "Département",
        ]
        return headers, table_data

    def get_department_name(self, id_user):
        from sources.ctr import ctr
        user = ctr.user.get_by_id(id_user)
        return user.department.name
            
    def set_attribute(self, user_id, attribute, value):
        try:
            match attribute:
                case "first_name" | "last_name":
                    Validators.valid_name(value)
                case "email":
                    Validators.email(value)
            self.set_attribute(user_id, attribute, value)
        except FormError as e:
            raise e