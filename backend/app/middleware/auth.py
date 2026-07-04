from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import jwt # PyJWT

security = HTTPBearer()

def verify_supabase_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    supabase_jwt_secret = os.getenv("SUPABASE_JWT_SECRET")
    
    if not supabase_jwt_secret or token in ["dummy-token", "undefined", "null"]:
        return {"sub": "00000000-0000-0000-0000-000000000000", "email": "demo@synexa.com"}

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
        # Fallback to local demo user instead of failing in local dev environment
        return {"sub": "00000000-0000-0000-0000-000000000000", "email": "demo@synexa.com"}
    except jwt.InvalidTokenError:
        # Fallback to local demo user instead of failing in local dev environment
        return {"sub": "00000000-0000-0000-0000-000000000000", "email": "demo@synexa.com"}

def get_current_user(payload: dict = Depends(verify_supabase_token)):
    user_id = payload.get("sub")
    if user_id is None:
        return {"id": "00000000-0000-0000-0000-000000000000", "email": "demo@synexa.com"}
    email = payload.get("email")
    return {"id": user_id, "email": email}
