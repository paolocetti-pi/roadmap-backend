from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserCreateSchema, UserLoginSchema, UserResponseSchema, TokenSchema
from services.user_service import user_service
from services.database import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .base_router import BaseRouter

class UserRouter(BaseRouter):
    def __init__(self):
        super().__init__(prefix="/users", tags=["users"])

    def setup_routes(self):
        self.router.add_api_route(
            "/register",
            self.register,
            methods=["POST"],
            response_model=UserResponseSchema
        )
        self.router.add_api_route(
            "/login",
            self.login,
            methods=["POST"],
            response_model=TokenSchema
        )

    def register(self, user_in: UserCreateSchema, db: Session = Depends(get_db)):
        db_user = user_service.get_user_by_email(db, user_in.email)
        if db_user:
            raise HTTPException(status_code=400, detail="El email ya está registrado")
        user = user_service.create_user(db, user_in)
        return user

    def login(self, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
        user = user_service.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        token_data = {"user_id": user.id, "email": user.email, "user_type": user.user_type.name}
        access_token = user_service.create_access_token(token_data)
        return {"access_token": access_token, "token_type": "bearer"}

# Dependencias de autenticación y autorización

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = user_service.verify_jwt_token(token)
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = user_service.get_user_by_email(db, payload.get("email"))
    if user is None:
        raise credentials_exception
    return user

def require_admin_user(current_user = Depends(get_current_user)):
    if not hasattr(current_user, "user_type") or current_user.user_type.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Acceso solo para administradores")
    return current_user

# Instancia global
user_router = UserRouter()
router = user_router.get_router() 