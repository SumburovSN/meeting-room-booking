class UserAlreadyExistsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class ForbiddenOperationError(Exception):
    pass