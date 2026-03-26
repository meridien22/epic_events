class EpicEventsError(Exception):
    """Classe de base pour toutes les erreurs spécifiques au CRM."""
    pass

class AuthError(EpicEventsError):
    """Erreur liée à la connexion ou au token."""
    pass

class DatabaseError(EpicEventsError):
    """Erreur lors d'une opération sur la base de données."""
    pass

class FileError(EpicEventsError):
    """Erreur lors d'une opération sur la base de données."""
    pass