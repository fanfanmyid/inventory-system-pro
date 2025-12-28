from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core import security

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    This function automatically:
    1. Extracts the token from the 'Authorization' header.
    2. Fails with 401 if the header is missing or malformed.
    3. Passes the token string to our PASETO verifier.
    """
    payload = security.verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload.get("sub") # Returns the username (subject)