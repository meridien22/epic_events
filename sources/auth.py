from sources.database import SessionLocal
from cryptography.hazmat.primitives import serialization
from private.parameter import parameter
from sources.models import User
from datetime import datetime, timedelta, timezone
import jwt
from sources.views import UserView

view = UserView()

def get_password():
    pwd = parameter["ssh_private_key_password"]
    return pwd.encode('utf-8')

def get_private_key():
    private_key = open(parameter["ssh_private_key_file"], 'r').read()
    return private_key.encode()

def get_private_key_ssh():
    return serialization.load_ssh_private_key(
         get_private_key(), 
         password=get_password()
    )

def get_public_key():
    public_key = open(parameter["ssh_public_key_file"], 'r').read()
    return public_key.encode()


def get_public_key_ssh():
    return serialization.load_ssh_public_key(
         get_public_key()
    )

def generate_token_from_id(id):
    with SessionLocal() as session:
        user = session.query(User).filter_by(id=id).first()
        if not user :
            return "Error"

    generate_token(id)

def generate_token_from_email(email, password):
    with SessionLocal() as session:
        user = session.query(User).filter_by(email=email).first()
        if not user or not user.check_password(password):
            return "Error"

        generate_token(user.id)

def generate_token(id_user):
    now = datetime.now(timezone.utc)
    
    access_payload = {
        "sub": id_user,
        "exp": now + timedelta(minutes=15),
        "type": "access",
        "department": user.department.id
    }
    
    refresh_payload = {
        "sub": id_user,
        "exp": now + timedelta(days=7),
        "type": "refresh"
    }

    access_token = jwt.encode(access_payload, key=get_private_key_ssh(), algorithm='RS256')
    refresh_token = jwt.encode(refresh_payload, key=get_private_key_ssh(), algorithm='RS256')

    with open(".env", "w") as f:
        f.write(f"EPIC_EVENTS_ACCESS_TOKEN={access_token}\n")
        f.write(f"EPIC_EVENTS_REFRESH_TOKEN={refresh_token}\n")

def refresh(refresh_token):
    try:
        header_data = jwt.get_unverified_header(refresh_token)
        payload = jwt.decode(
            refresh_token, key=get_public_key_ssh(), 
            algorithms=[header_data['alg'], ]
        )
        generate_token(payload['sub'])
    except jwt.ExpiredSignatureError:
        view.display_error("Votre session a expiré. Veuillez vous reconnecter.")
    except Exception as error:
        view.display_error("Votre session est invalide. Veuillez vous reconnecter.")
    
    