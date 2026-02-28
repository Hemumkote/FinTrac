from datetime import timedelta
from venv import create
from fastapi import APIRouter, HTTPException
from jose import JWTError, jwt

from Fintrac_backend.core.security import create_access_token
from core.config import settings


refresh_route = APIRouter(prefix="/api/v1/user/refresh", tags=["refresh"])

# refresh endpoint


@refresh_route.post("", status_code=200, summary="refresh token refetch")
async def refresh_access_token(refresh_token: str):
    try:
        payload = jwt.decode(
            refresh_token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        if not payload.get("refresh"):
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        userId = payload.get("sub")
        # optional check if the refresh_token is black listed int he Redis/ DB

        new_access_token = create_access_token(
            data={"sub": userId},
            expires_delta=timedelta(minutes=settings.JWT_EXPIRY_MINUTES),
        )
        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
