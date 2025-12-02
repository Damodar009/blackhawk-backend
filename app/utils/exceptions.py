from fastapi import HTTPException, status

def raise_error(
    message: str,
    status_code: int = status.HTTP_400_BAD_REQUEST
):
    """
    Raise a standardized HTTPException with consistent error response format.
    """
    raise HTTPException(
        status_code=status_code,
        detail={
            "status_code": status_code,
            "error_message": message
        }
    )

class AuthException(HTTPException):
    """Base authentication exception"""
    def __init__(self, message: str, status_code: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(
            status_code=status_code,
            detail={
                "status_code": status_code,
                "error_message": message
            },
            headers={"WWW-Authenticate": "Bearer"}
        )


class AuthenticationError(AuthException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class TokenExpiredError(AuthException):
    def __init__(self, message: str = "Token has expired"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class InsufficientPermissionsError(AuthException):
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class NotFoundError(HTTPException):
    def __init__(self, message: str = "User not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "error_message": message
            }
        )


class AlreadyExistsError(HTTPException):
    def __init__(self, message: str = "User already exists"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "status_code": status.HTTP_409_CONFLICT,
                "error_message": message
            }
        )


class InvalidCredentialsError(HTTPException):
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status_code": status.HTTP_401_UNAUTHORIZED,
                "error_message": message
            },
            headers={"WWW-Authenticate": "Bearer"}
        )
