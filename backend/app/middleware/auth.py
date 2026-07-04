from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import jwt # PyJWT

security = HTTPBearer()

def verify_supabase_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    supabase_jwt_secret = os.getenv("SUPABASE_JWT_SECRET")
    
    if not supabase_jwt_secret:
        raise HTTPException(status_code=500, detail="Missing SUPABASE_JWT_SECRET environment variable")

    try:
        # Supabase uses HS256 algorithm by default
        payload = jwt.decode(
            token,
            supabase_jwt_secret,
            algorithms=["HS256"],
            options={"verify_aud": False}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(payload: dict = Depends(verify_supabase_token)):
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid user context in token")
    email = payload.get("email")
    return {"id": user_id, "email": email}
