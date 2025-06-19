from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
import os
import requests
from urllib.parse import urlencode
from services.database import get_db
from services.user_service import user_service
from services.sso_service import SSOService

router = APIRouter(tags=["SSO"])

# --- Google SSO ---
@router.get("/login/google")
def login_google():
    params = {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return RedirectResponse(url)

@router.get("/auth/google/callback")
def auth_google_callback(request: Request, code: str, db: Session = Depends(get_db)):
    sso_service = SSOService()
    try:
        user, token = sso_service.handle_google_callback(code, db)
        return JSONResponse({"user": user, "access_token": token})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Microsoft SSO ---
@router.get("/login/microsoft")
def login_microsoft():
    params = {
        "client_id": os.getenv("MICROSOFT_CLIENT_ID"),
        "response_type": "code",
        "redirect_uri": os.getenv("MICROSOFT_REDIRECT_URI"),
        "response_mode": "query",
        "scope": "openid email profile User.Read",
        "prompt": "select_account"
    }
    tenant = os.getenv("MICROSOFT_TENANT_ID", "common")
    url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?{urlencode(params)}"
    return RedirectResponse(url)

@router.get("/auth/microsoft/callback")
def auth_microsoft_callback(request: Request, code: str, db: Session = Depends(get_db)):
    sso_service = SSOService()
    try:
        user, token = sso_service.handle_microsoft_callback(code, db)
        return JSONResponse({"user": user, "access_token": token})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 