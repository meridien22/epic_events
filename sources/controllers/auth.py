from sources.database.postgres import SessionLocal
from cryptography.hazmat.primitives import serialization
from private.parameter import parameter
from sources.models import User, Permission, Department, Event
from datetime import datetime, timedelta, timezone
import jwt
from sources.views import UserView
from functools import wraps
import click
from decouple import config
from sqlalchemy import select, exists

class _Token:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.user_id = None
        self.department_id = None

_token = _Token()

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
            "exp": now + timedelta(minutes=10),
            "type": "access",
            "department": user.department.id
        }
        
        refresh_payload = {
            "sub": str(id_user),
            "exp": now + timedelta(days=30),
            "type": "refresh"
        }

        access_token = jwt.encode(access_payload, key=get_private_key_ssh(), algorithm='RS256')
        refresh_token = jwt.encode(refresh_payload, key=get_private_key_ssh(), algorithm='RS256')

        # écriture des tokens dans le fichier .env
        with open(".env", "w") as f:
            f.write(f"EPIC_EVENTS_ACCESS_TOKEN={access_token}\n")
            f.write(f"EPIC_EVENTS_REFRESH_TOKEN={refresh_token}\n")

        # écriture des tokens dans la classe
        _token.access_token = access_token
        _token.refresh_token = refresh_token
        _token.user_id = id_user
        _token.department_id = user.department.id

def is_valid_token(token, type):
    try:
        header_data = jwt.get_unverified_header(token)
        payload = jwt.decode(
            token,
            key=get_public_key_ssh(), 
            algorithms=[header_data['alg'], ]
        )
        # on vérifie le type du token pour éviter d'utiliser un refresh à la place d'un access
        if not payload.get('type') == type:
            return False
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
    if is_valid_token(_token.access_token, "access"):
        return True
    else:
        UserView.display_info("Vous êtes déconnecté. Tentative de reconnexion....")
        if is_valid_token(_token.refresh_token, "refresh"):
            payload = get_payload(_token.refresh_token)
            generate_token(payload.get('sub'))
            return True
        else:
            return False
            
def login_required(f):
    """Gestion de l'authentification"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        _token.access_token = config("EPIC_EVENTS_ACCESS_TOKEN", default=None)
        _token.refresh_token = config("EPIC_EVENTS_REFRESH_TOKEN", default=None)
        if not is_valid_tokens_env() or _token.access_token is None or _token.refresh_token is None:
            UserView.display_error("Erreur d'authentification.")
            raise click.Abort()
        else:
            # si le token est valide, on récupère le user et le département
            payload = get_payload(_token.access_token)
            _token.user_id = payload.get('sub')
            _token.department_id = payload.get('department')
        return f(*args, **kwargs)
    return wrapper

def permission_required(permission):
    """Gestion des autorisations"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            with SessionLocal() as session:
                query = (
                    select(Permission.name)
                    .join(Permission.departments)
                    .where(Department.id == _token.department_id)
                )
                permissions = session.execute(query).scalars().all()
                if permission not in permissions:
                    UserView.display_error("Opération non autorisée.")
                    raise click.Abort()
            return f(*args, **kwargs)
        return wrapper
    return decorator

def owns_event(f):
    """Gestion de l'Object Access sur event"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        with SessionLocal() as session:
            # click ajouter les paramètres de la commande comme des arguments de la fonction
            event_id = kwargs.get('event_id')
            # on vérifie si l'event existe dans la base
            query = select(exists().where(Event.id == event_id))
            result = session.execute(query).scalar()
            if not result:
                UserView.display_error("Evénement inconnu dans la base")
                raise click.Abort()
            # on vérifie que l'utilisateur est bien le support de l'event
            event = session.query(Event).filter_by(id=event_id).first()
            if not event.support_id == _token.user_id:
                UserView.display_error("Accès refusé : vous devez être le gestionnaire de l'événement pour pouvoir le modifier")
                raise click.Abort()
