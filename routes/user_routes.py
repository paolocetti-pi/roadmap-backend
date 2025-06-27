from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreateSchema, UserLoginSchema, UserResponseSchema, TokenSchema
from services.user_service import user_service
from services.database import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .base_router import BaseRouter
import logging

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

    async def register(self, user_in: UserCreateSchema, db: AsyncSession = Depends(get_db)):
        logging.info(f"Registering user with email: {user_in.email}")
        db_user = await user_service.get_user_by_email(db, user_in.email)
        if db_user:
            logging.warning(f"Registration attempt for existing email: {user_in.email}")
            raise HTTPException(status_code=400, detail="El email ya está registrado")
        user = await user_service.create_user(db, user_in)
        logging.info(f"User registered successfully: {user.email}")
        return user

    async def login(self, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
        logging.info(f"Login attempt for user: {form_data.username}")
        user = await user_service.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            logging.warning(f"Failed login attempt for user: {form_data.username}")
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        token_data = {"user_id": user.id, "email": user.email, "user_type": user.user_type.name}
        access_token = user_service.create_access_token(token_data)
        logging.info(f"User logged in successfully: {user.email}")
        return {"access_token": access_token, "token_type": "bearer"}

# Dependencias de autenticación y autorización

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = user_service.verify_jwt_token(token)
        user_id: int = payload.get("user_id")
        if user_id is None:
            logging.error("User ID not in token payload")
            raise credentials_exception
    except Exception as e:
        logging.error(f"Token validation error: {e}")
        raise credentials_exception
    user = await user_service.get_user_by_email(db, payload.get("email"))
    if user is None:
        logging.error(f"User not found for email: {payload.get('email')}")
        raise credentials_exception
    logging.debug(f"Current user retrieved: {user.email}")
    return user

def require_admin_user(current_user = Depends(get_current_user)):
    if not hasattr(current_user, "user_type") or current_user.user_type.name != "ADMIN":
        logging.warning(f"Admin access denied for user: {current_user.email}")
        raise HTTPException(status_code=403, detail="Acceso solo para administradores")
    logging.debug(f"Admin access granted for user: {current_user.email}")
    return current_user

# Instancia global
user_router = UserRouter()
router = user_router.get_router() 