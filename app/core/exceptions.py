class UserNotFoundError(Exception):
    """Exception raised when a user is not found in the database."""

    pass


class UserAlreadyExistsError(Exception):
    """Exception raised when attempting to create a user that already exists."""

    pass
