from sources.database.postgres import SessionLocal
from cryptography.hazmat.primitives import serialization
from private.parameter import parameter
from sources.models import User, Permission, Department
from datetime import datetime, timedelta, timezone
import jwt
from sources.views import UserView
from functools import wraps
import click
from decouple import config
from sqlalchemy import select, exists


def get_private_key_ssh():
    pwd = parameter["ssh_private_key_password"]
    private_key = open(parameter["ssh_private_key_file"], 'r').read()
    return serialization.load_ssh_private_key(
         private_key.encode(), 
         password=pwd.encode('utf-8')
    )

def get_public_key_ssh():
    public_key = open(parameter["ssh_public_key_file"], 'r').read()
    return serialization.load_ssh_public_key(
         public_key.encode()
    )

# def generate_token_from_id(id_user):
#     with SessionLocal() as session:
#         user = session.query(User).filter_by(id=id_user).first()
#         if not user :
#             return "Error"
#     generate_token(id)

def generate_token_from_email_password(email, password):
    with SessionLocal() as session:
        user = session.query(User).filter_by(email=email).first()
        if not user or not user.check_password(password):
            return "Error"
        generate_token(user.id)

def generate_token(id_user):
    with SessionLocal() as session:
        now = datetime.now(timezone.utc)
        user = session.query(User).filter_by(id=id_user).first()

        access_payload = {
            "sub": str(id_user),
            "exp": now + timedelta(minutes=1),
            "type": "access",
            "department": user.department.id
        }
        
        refresh_payload = {
            "sub": str(id_user),
            "exp": now + timedelta(days=1),
            "type": "refresh"
        }

        access_token = jwt.encode(access_payload, key=get_private_key_ssh(), algorithm='RS256')
        refresh_token = jwt.encode(refresh_payload, key=get_private_key_ssh(), algorithm='RS256')

        # écriture des tokens dans le fichier .env
        with open(".env", "w") as f:
            f.write(f"EPIC_EVENTS_ACCESS_TOKEN={access_token}\n")
            f.write(f"EPIC_EVENTS_REFRESH_TOKEN={refresh_token}\n")

def is_valid_token(token):
    try:
        header_data = jwt.get_unverified_header(token)
        payload = jwt.decode(
            token,
            key=get_public_key_ssh(), 
            algorithms=[header_data['alg'], ]
        )
        # on vérifie aussi que l'id_user du payload existe encore dans la DB
        user_id = payload.get('sub')
        query = select(exists().where(User.id == user_id))
        with SessionLocal() as session:
            result = session.execute(query).scalar()
            if not result:
                return False
    except jwt.ExpiredSignatureError:
        return False
    except Exception as error:
        return False
    return True

def get_payload(token):
    header_data = jwt.get_unverified_header(token)
    payload = jwt.decode(token, key=get_public_key_ssh(), algorithms=[header_data['alg'], ])
    return payload

def is_valid_tokens_env():
    token = config("EPIC_EVENTS_ACCESS_TOKEN", default=None)
    if token is None :
        return False
    else:
        if is_valid_token(token):
            return True
        else:
            token = config("EPIC_EVENTS_REFRESH_TOKEN", default=None)
            if token is None :
                return False
            else :
                UserView.display_info("Vous êtes déconnecté. Tentative de reconnexion....")
                if is_valid_token(token):
                    payload = get_payload(token)
                    generate_token(payload.get('sub'))
                    return True
                else:
                    return False
                
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not is_valid_tokens_env():
            UserView.display_error("Erreur d'authentification.")
            raise click.Abort()
        token = config("EPIC_EVENTS_ACCESS_TOKEN")
        payload = get_payload(token)
        kwargs['user_id'] = payload.get('sub')
        kwargs['department_id'] = payload.get('department')
        return f(*args, **kwargs)
    return wrapper

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            with SessionLocal() as session:
                department_id = kwargs.get('department_id')

                query = (
                    select(Permission.name)
                    .join(Permission.departments)
                    .where(Department.id == department_id)
                )
                result = session.execute(query).scalars().all()

                print(result)

                # if user_dept not in allowed_departments:
                #     click.secho(
                #         f"🚫 Accès refusé. Cette action est réservée au département : {', '.join(allowed_departments)}", 
                #         fg="red"
                #     )
                #     raise click.Abort()
                
                kwargs.pop('user_id', None)
                kwargs.pop('department_id', None)
            return f(*args, **kwargs)
        return wrapper
    return decorator