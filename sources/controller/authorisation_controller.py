from sources.controller.token_controller import current_session, token
from functools import wraps
from decouple import config
from sources.exceptions import AuthError, DatabaseError
from sources.dao.base_dao import SessionLocal
from sources.dao import DAO
import click

def login_required(f):
    """Gestion de l'authentification"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        current_session.access_token = config("EPIC_EVENTS_ACCESS_TOKEN", default=None)
        current_session.refresh_token = config("EPIC_EVENTS_REFRESH_TOKEN", default=None)
        if not current_session.access_token or not current_session.refresh_token:
            # raise AuthError("Aucun token trouvé. Veuillez vous connecter (login).")
            click.secho("Aucun token trouvé. Veuillez vous connecter (login).", bold=True)
            raise click.Abort()
        if not token.is_valid_access_refresh() :
            # raise AuthError("Erreur d'authentification : session invalide ou expirée.")
            click.secho("Erreur d'authentification : session invalide ou expirée.", bold=True)
            raise click.Abort()
        # si le token est valide, on récupère le user et le département
        payload = token.get_payload(current_session.access_token)
        current_session.user_id = payload.get('sub')
        current_session.department_id = payload.get('department')
        return f(*args, **kwargs)
    return wrapper

def permission_required(permission):
    """Gestion des autorisations"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            with SessionLocal() as session:
                dao = DAO(session)
                permissions = dao.departement.get_permission(current_session.department_id)
                if permission not in permissions:
                    # raise AuthError("Opération non autorisée.")
                    click.secho("Opération non autorisée.", bold=True)
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
            dao = DAO(session)
            if not dao.event.exists(event_id):
                # raise DatabaseError("Evénement inconnu dans la base.")
                click.secho("Evénement inconnu dans la base.", bold=True)
                raise click.Abort()
            # on vérifie que l'utilisateur est bien le support de l'event
            event = dao.event.get_by_id(event_id)
            if not event.support_id == current_session.user_id:
                # raise AuthError("Accès refusé : vous devez être le gestionnaire de l'événement pour pouvoir le modifier.")
                click.secho("Accès refusé : vous devez être le gestionnaire de l'événement pour pouvoir le modifier.", bold=True)
                raise click.Abort()
        return f(*args, **kwargs)
    return wrapper