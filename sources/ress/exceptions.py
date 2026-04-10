class EpicEventsError(Exception):
    """Base class for all CRM-specific errors."""
    pass


class AuthError(EpicEventsError):
    """Error related to the connection or the token."""
    pass


class DatabaseError(EpicEventsError):
    """Error during a database operation."""
    pass


class FileError(EpicEventsError):
    """Error during a file operation."""
    pass


class FormError(EpicEventsError):
    """Error during a form operation."""
    pass


class NotFoundError(EpicEventsError):
    """Error when the search returns no records."""
    pass
