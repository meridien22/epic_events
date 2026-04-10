from sources.dao.base_dao import SessionLocal
from sources.dao import DAO
from sources.ress.exceptions import AuthError, DatabaseError, FileError
from datetime import datetime, timedelta, timezone
import jwt
from sources.ress.security import get_private_key_ssh, get_public_key_ssh


class Session:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.user_id = None
        self.department_id = None
        self.first_name = None
        self.last_name = None


current_session = Session()


class Token:
    def generate_token_from_email_password(self, email, password):
        with SessionLocal() as session:
            dao = DAO(session)
            user = dao.user.get_by_mail(email)
            if not user or not user.check_password(password):
                raise AuthError("Email ou mot de passe incorrect.")
            self.generate_token(user.id)

    def generate_token(self, id_user):
        with SessionLocal() as session:
            now = datetime.now(timezone.utc)
            dao = DAO(session)
            user = dao.user.get_by_id(id_user)

            access_payload = {
                "sub": str(id_user),
                "exp": now + timedelta(minutes=10),
                "type": "access",
                "department": user.department.id
            }

            refresh_payload = {
                "sub": str(id_user),
                "exp": now + timedelta(days=0.5),
                "type": "refresh"
            }

            access_token = jwt.encode(access_payload, key=get_private_key_ssh(), algorithm='RS256')
            refresh_token = jwt.encode(refresh_payload, key=get_private_key_ssh(), algorithm='RS256')

            # écriture des tokens dans le fichier .env
            try:
                with open(".env", "w") as f:
                    f.write(f"EPIC_EVENTS_ACCESS_TOKEN={access_token}\n")
                    f.write(f"EPIC_EVENTS_REFRESH_TOKEN={refresh_token}\n")
            except OSError:
                raise FileError("Impossible d'écrire le fichier de session sur le disque.")

            # écriture des tokens dans la classe
            current_session.access_token = access_token
            current_session.refresh_token = refresh_token
            current_session.user_id = id_user
            current_session.department_id = user.department.id
            current_session.first_name = user.first_name
            current_session.last_name = user.last_name

            return user

    def get_payload(self, token):
        header_data = jwt.get_unverified_header(token)
        payload = jwt.decode(token, key=get_public_key_ssh(), algorithms=[header_data['alg'], ])
        return payload

    def is_valid_access_refresh(self):
        try:
            self.is_valid(current_session.access_token, "access")
            return True
        except AuthError:
            try:
                self.is_valid(current_session.refresh_token, "refresh")
                payload = self.get_payload(current_session.refresh_token)
                self.generate_token(payload.get('sub'))
                return True
            except AuthError as refresh_error:
                raise AuthError(str(refresh_error))
            except OSError as file_error:
                raise FileError(str(file_error))

    def is_valid(self, token, type):
        try:
            header_data = jwt.get_unverified_header(token)
            payload = jwt.decode(
                token,
                key=get_public_key_ssh(),
                algorithms=[header_data['alg'], ]
            )
            # on vérifie le type du token pour éviter d'utiliser un refresh à la place d'un access
            if not payload.get('type') == type:
                raise AuthError("Type de token inattendu.")
            with SessionLocal() as session:
                # on vérifie aussi que l'id_user du payload existe encore dans la DB
                dao = DAO(session)
                user = dao.user.get_by_id(payload.get('sub'))
                if not user:
                    raise DatabaseError("Utilisateur inconnu.")
            return True
        except jwt.ExpiredSignatureError:
            raise AuthError("Token expiré.")
        except Exception:
            raise AuthError("Token invalide.")


token = Token()
