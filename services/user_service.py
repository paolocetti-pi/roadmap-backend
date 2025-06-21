from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt  # PyJWT
from sqlalchemy.orm import Session
from models.user import User, UserType
from schemas.user import UserCreateSchema
from fastapi import HTTPException, status
import os
import logging

# Configuración de hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class UserService:
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        logging.debug(f"Querying for user with email: {email}")
        return db.query(User).filter(User.email == email).first()

    def create_user(self, db: Session, user_in: UserCreateSchema) -> User:
        logging.info(f"Creating user with email: {user_in.email}")
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
        logging.info(f"User created successfully with email: {db_user.email}")
        return db_user

    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        logging.info(f"Authenticating user: {email}")
        user = self.get_user_by_email(db, email)
        if not user:
            logging.warning(f"Authentication failed: User not found for email {email}")
            return None
        if not self.verify_password(password, user.password):
            logging.warning(f"Authentication failed: Invalid password for user {email}")
            return None
        logging.info(f"User authenticated successfully: {email}")
        return user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        logging.info(f"Creating access token for user: {data.get('email')}")
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logging.debug("Access token created successfully")
        return encoded_jwt

    def verify_jwt_token(self, token: str):
        try:
            logging.debug("Verifying JWT token")
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            logging.debug(f"Token payload: {payload}")
            return payload
        except jwt.ExpiredSignatureError:
            logging.warning("Token verification failed: ExpiredSignatureError")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.PyJWTError:
            logging.warning("Token verification failed: PyJWTError")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def get_password_hash(self, password: str) -> str:
        logging.debug("Hashing password")
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        logging.debug("Verifying password")
        return pwd_context.verify(plain_password, hashed_password)

# Singleton
user_service = UserService() 