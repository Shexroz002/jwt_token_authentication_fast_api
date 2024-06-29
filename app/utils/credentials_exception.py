from fastapi import HTTPException
from starlette import status


def unauthorized_exception(details: str = "Could not Validate Credentials") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=details,
        headers={"WWW-Authenticate": "Bearer"}
    )


def login_exception(details: str = "Incorrect username or password") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=details
    )
