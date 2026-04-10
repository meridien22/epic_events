from contextlib import contextmanager
from sqlalchemy.exc import IntegrityError
from sources.ress.session import SessionLocal
from sources.ress.view import View
import sentry_sdk
from private.parameter import parameter
from sources.ress.exceptions import (EpicEventsError, DatabaseError, FormError,
                                     AuthError, FileError, NotFoundError)
import sys

sentry_sdk.init(
    dsn=parameter["sentry_dns"],
    send_default_pii=True,
)


@contextmanager
def transaction_scope():
    """Manages the lifecycle of an SQL transaction with error handling."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except IntegrityError:
        session.rollback()
        raise DatabaseError("Donnée déjà existante ou non autorisé.")
    except EpicEventsError as e:
        session.rollback()
        raise e
    except Exception:
        session.rollback()
        raise DatabaseError("Une erreur inattendue est survenue.")
    finally:
        session.close()


@contextmanager
def view_scope():
    """Manages the lifecycle of an SQL transaction (SELECT only) with error handling."""
    session = SessionLocal()
    try:
        yield session
    except EpicEventsError as e:
        raise e
    except Exception as e:
        raise e
    finally:
        session.close()


ERROR_LABELS = {
    "DatabaseError": "ERREUR SQL",
    "FormError": "SAISIE INCORRECTE",
    "AuthError": "ACCES REFUSE",
    "FileError": "ERREUR FICHIER",
    "NotFoundError": "ECHEC RECHERCHE",
}


@contextmanager
def auth_scope():
    """Manages the display of errors for authentication and authorization decorators."""
    session = SessionLocal()
    try:
        yield session
    except AuthError as e:
        class_name = e.__class__.__name__
        friendly_name = ERROR_LABELS.get(class_name, class_name)
        View.display_info(f"[{friendly_name}] : {str(e)}")
        sentry_sdk.capture_exception(e)
        sys.exit()
    except Exception as e:
        View.display_error("[ERREUR CRITIQUE] : Une erreur inattendue est survenue.")
        sentry_sdk.capture_exception(e)


@contextmanager
def cmd_scope():
    """Manages the display of errors for CLI commands."""
    try:
        yield
    except DatabaseError as e:
        class_name = e.__class__.__name__
        friendly_name = ERROR_LABELS.get(class_name, class_name)
        View.display_error(f"[{friendly_name}] : {str(e)}")
        sentry_sdk.capture_exception(e)
    except FormError as e:
        class_name = e.__class__.__name__
        friendly_name = ERROR_LABELS.get(class_name, class_name)
        View.display_info(f"[{friendly_name}] : {str(e)}")
    except AuthError as e:
        class_name = e.__class__.__name__
        friendly_name = ERROR_LABELS.get(class_name, class_name)
        View.display_error(f"[{friendly_name}] : {str(e)}")
        sentry_sdk.capture_exception(e)
    except FileError as e:
        class_name = e.__class__.__name__
        friendly_name = ERROR_LABELS.get(class_name, class_name)
        View.display_error(f"[{friendly_name}] : {str(e)}")
    except NotFoundError as e:
        class_name = e.__class__.__name__
        friendly_name = ERROR_LABELS.get(class_name, class_name)
        View.display_info(f"[{friendly_name}] : {str(e)}")
    except Exception as e:
        View.display_error("[ERREUR CRITIQUE] : Une erreur inattendue est survenue.")
        sentry_sdk.capture_exception(e)
