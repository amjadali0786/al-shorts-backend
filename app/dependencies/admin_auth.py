from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.core.admin_config import ADMIN_USERNAME, ADMIN_PASSWORD

security = HTTPBasic()

def admin_auth(
    request: Request,
    credentials: HTTPBasicCredentials = Depends(security)
):
    # ✅ Allow preflight requests
    if request.method == "OPTIONS":
        return True

    if (
        credentials.username != ADMIN_USERNAME
        or credentials.password != ADMIN_PASSWORD
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return True
