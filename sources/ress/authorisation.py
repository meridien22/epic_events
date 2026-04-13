from sources.ress.token import current_session, token
from functools import wraps
from decouple import config
from sources.dao import DAO
from sources.ress.view import View
from sources.ress.exceptions import AuthError
from sources.ress.context_manager import auth_scope


def login_required(f):
    """Authentication verification."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        with auth_scope():
            current_session.access_token = config("EPIC_EVENTS_ACCESS_TOKEN", default=None)
            current_session.refresh_token = config("EPIC_EVENTS_REFRESH_TOKEN", default=None)
            if not current_session.access_token or not current_session.refresh_token:
                raise AuthError("Aucun token trouvé. Veuillez vous connecter (login).")
            token.is_valid_access_refresh()
            # si le token est valide, on récupère le user et le département
            payload = token.get_payload(current_session.access_token)
            current_session.user_id = payload.get('sub')
            current_session.department_id = payload.get('department')
            return f(*args, **kwargs)
    return wrapper


def read_user_from_token():
    """Reads the token's user information if the token is valid."""
    with auth_scope() as session:
        current_session.access_token = config("EPIC_EVENTS_ACCESS_TOKEN", default=None)
        current_session.refresh_token = config("EPIC_EVENTS_REFRESH_TOKEN", default=None)
        if not current_session.access_token or not current_session.refresh_token:
            return 'Aucun utilisateur connecté. Veuillez vous connecter (login).'
        try:
            token.is_valid_access_refresh()
        except Exception:
            return 'Aucun utilisateur connecté. Veuillez vous connecter (login).'
        # si le token est valide, on récupère le user
        payload = token.get_payload(current_session.access_token)
        dao = DAO(session)
        user = dao.user.get_by_id(payload.get('sub'))
        return (f'Utilisateur connecté : {user.first_name} {user.last_name} ({user.department.name})')


def permission_required(permission):
    """Checking permissions."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            with auth_scope() as session:
                dao = DAO(session)
                permissions = dao.department.get_permission(current_session.department_id)
                if permission not in permissions:
                    # View.display_info("Opération non autorisée.")
                    # return
                    raise AuthError("Opération non autorisée.")
            return f(*args, **kwargs)
        return wrapper
    return decorator


def owns_event(f):
    """Checking Object Access on event"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        with auth_scope() as session:
            # click ajouter les paramètres de la commande comme des arguments de la fonction
            event_id = kwargs.get('event_id')
            # on vérifie si l'event existe dans la base
            dao = DAO(session)
            if not dao.event.exists(event_id):
                View.display_info("Evénement inconnu dans la base.")
                return
            # on vérifie que l'utilisateur est bien le support de l'event
            event = dao.event.get_by_id(event_id)
            if not event.support_id == current_session.user_id:
                messsage = "Accès refusé : vous devez être le gestionnaire de l'événement pour pouvoir le modifier."
                View.display_info(messsage)
                return
        return f(*args, **kwargs)
    return wrapper


def owns_client(f):
    """Checking Object Access on client"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        with auth_scope() as session:
            # click ajouter les paramètres de la commande comme des arguments de la fonction
            client_id = kwargs.get('client_id')
            # on vérifie si le client existe dans la base
            dao = DAO(session)
            if not dao.client.exists(client_id):
                View.display_info("Client inconnu dans la base.")
                return
            # on vérifie que l'utilisateur est bien le support de l'event
            client = dao.client.get_by_id(client_id)
            if not client.commercial_id == int(current_session.user_id):
                View.display_info("Accès refusé : vous devez être le gestionnaire du client pour pouvoir le modifier.")
                return
        return f(*args, **kwargs)
    return wrapper


def owns_contrat_or_permission(permission):
    """Checking Object Access on contract"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            with auth_scope() as session:
                dao = DAO(session)
                # click ajouter les paramètres de la commande comme des arguments de la fonction
                contract_id = kwargs.get('contract_id')
                # on vérifie si le client existe dans la base
                dao = DAO(session)
                if not dao.contract.exists(contract_id):
                    View.display_info("Contrat inconnu dans la base.")
                    return
                # on vérifie la permission
                permissions = dao.department.get_permission(current_session.department_id)
                if permission in permissions:
                    has_permission = True
                else:
                    has_permission = False
                # on vérifie que l'utilisateur est bien le support de l'event
                contract = dao.contract.get_by_id(contract_id)
                client = dao.client.get_by_id(contract.client_id)
                if client.commercial_id == int(current_session.user_id):
                    is_owner = True
                else:
                    is_owner = False
                # on récupère le nom du département
                department = dao.department.get_by_id(current_session.department_id)
                department_name = department.name

                access = False
                if department_name == 'Management' and has_permission:
                    access = True
                if department_name == 'Sales' and has_permission and is_owner:
                    access = True

                if not access:
                    View.display_info("Accès refusé : vous n'êtes pas autorisé à modifier ce contrat.")
                    return
            return f(*args, **kwargs)
        return wrapper
    return decorator
