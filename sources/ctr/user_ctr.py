from sources.dao import DAO
from sources.ress.validators import Validators
from sources.ress.exceptions import FormError
from sources.ctr.base_ctr import BaseCTR
from sources.ress.context_manager import transaction_scope


class UserCTR(BaseCTR):
    def __init__(self):
        super().__init__("user")

    def add(self, first_name, last_name, email, password, department_id):
        self.validate_attribute("first_name", first_name)
        self.validate_attribute("last_name", last_name)
        self.validate_attribute("email", email)
        self.validate_attribute("password", password)
        with transaction_scope() as session:
            dao = DAO(session)
            dao.user.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                department_id=department_id,
                password=password
            )

    def get_table_with_headers(self, users): 
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
        user = ctr.user.get(id_user, "department")
        return user.department.name
            
    def set_attribute_user(self, user_id, attribute, value):
            self.validate_attribute(attribute, value)
            self.set_attribute(user_id, attribute, value)

    def validate_attribute(self, attribute, value):
        try:
            match attribute:
                case "first_name":
                    Validators.string_len(value,"prénom",0, 50)
                case "last_name":
                    Validators.string_len(value,"nom",0, 50)
                case "email":
                    Validators.email(value)
                case "password":
                    Validators.valid_password(value)
        except FormError as e:
            raise e