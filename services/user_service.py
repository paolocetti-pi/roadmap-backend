from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt  # PyJWT
from sqlalchemy.orm import Session
from models.user import User, UserType
from schemas.user import UserCreateSchema
from fastapi import HTTPException, status
import os

# Configuración de hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class UserService:
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create_user(self, db: Session, user_in: UserCreateSchema) -> User:
        hashed_password = self.get_password_hash(user_in.password)
        db_user = User(
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            email=user_in.email,
            password=hashed_password,
            user_type_id=user_in.user_type_id
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        user = self.get_user_by_email(db, email)
        if not user or not self.verify_password(password, user.password):
            return None
        return user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_jwt_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

# Singleton
user_service = UserService() 