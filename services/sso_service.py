import os
import httpx
from services.user_service import user_service
from models.user import User
from schemas.user import UserCreateSchema
from sqlalchemy.ext.asyncio import AsyncSession
import logging

class SSOService:
    async def handle_google_callback(self, code: str, db: AsyncSession):
        logging.info("Handling Google callback")
        # Intercambiar el código por un token
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
            "grant_type": "authorization_code"
        }
        logging.debug("Requesting token from Google")
        async with httpx.AsyncClient() as client:
            token_resp = await client.post(token_url, data=data)
        if not token_resp.is_success:
            logging.error(f"Error getting token from Google: {token_resp.text}")
            raise Exception("Error al obtener el token de Google")
        tokens = token_resp.json()
        id_token = tokens.get("id_token")
        if not id_token:
            logging.error("id_token not in Google response")
            raise Exception("No se recibió id_token de Google")
        # Decodificar el id_token
        logging.debug("Decoding Google id_token")
        userinfo = await self.decode_google_id_token(id_token)
        # Registrar o actualizar usuario
        logging.info(f"Registering or updating user from Google SSO: {userinfo.get('email')}")
        user, token = await self.register_or_update_user(userinfo, db, provider="google")
        return user, token

    async def decode_google_id_token(self, id_token: str):
        logging.debug("Validating Google id_token")
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}")
        if not resp.is_success:
            logging.error(f"Invalid Google id_token: {resp.text}")
            raise Exception("id_token de Google inválido")
        return resp.json()

    async def handle_microsoft_callback(self, code: str, db: AsyncSession):
        logging.info("Handling Microsoft callback")
        tenant = os.getenv('MICROSOFT_TENANT_ID') or 'common'
        token_url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
        data = {
            "client_id": os.getenv("MICROSOFT_CLIENT_ID"),
            "scope": "openid email profile User.Read",
            "code": code,
            "redirect_uri": os.getenv("MICROSOFT_REDIRECT_URI"),
            "grant_type": "authorization_code",
            "client_secret": os.getenv("MICROSOFT_CLIENT_SECRET")
        }
        logging.debug("Requesting token from Microsoft")
        async with httpx.AsyncClient() as client:
            token_resp = await client.post(token_url, data=data)
        if not token_resp.is_success:
            logging.error(f"Error getting token from Microsoft: {token_resp.text}")
            raise Exception("Error al obtener el token de Microsoft")
        tokens = token_resp.json()
        access_token = tokens.get("access_token")
        if not access_token:
            logging.error("access_token not in Microsoft response")
            raise Exception("No se recibió access_token de Microsoft")
        # Obtener info del usuario
        logging.debug("Getting user info from Microsoft Graph API")
        userinfo = await self.get_microsoft_userinfo(access_token)
        logging.info(f"Registering or updating user from Microsoft SSO: {userinfo.get('mail') or userinfo.get('userPrincipalName')}")
        user, token = await self.register_or_update_user(userinfo, db, provider="microsoft")
        return user, token

    async def get_microsoft_userinfo(self, access_token: str):
        headers = {"Authorization": f"Bearer {access_token}"}
        logging.debug("Requesting user info from Microsoft Graph API")
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://graph.microsoft.com/v1.0/me", headers=headers)
        if not resp.is_success:
            logging.error(f"Could not get user info from Microsoft: {resp.text}")
            raise Exception("No se pudo obtener info de usuario de Microsoft")
        return resp.json()

    async def register_or_update_user(self, userinfo: dict, db: AsyncSession, provider: str):
        logging.info(f"Looking for existing user with email: {userinfo.get('email')}")
        if provider == "google":
            email = userinfo.get("email")
            first_name = userinfo.get("given_name", "")
            last_name = userinfo.get("family_name", "")
        elif provider == "microsoft":
            email = userinfo.get("mail") or userinfo.get("userPrincipalName")
            first_name = userinfo.get("givenName", "")
            last_name = userinfo.get("surname", "")
        else:
            logging.error(f"Unsupported SSO provider: {provider}")
            raise Exception("Proveedor SSO no soportado")
        if not email:
            logging.error("Could not get user email from provider")
            raise Exception("No se pudo obtener el email del usuario")
        # Buscar usuario existente
        logging.info(f"Looking for existing user with email: {email}")
        user = await user_service.get_user_by_email(db, email)
        if user:
            # Usuario ya existe, generar token
            logging.info(f"User {email} already exists. Generating token.")
            user_dict = user.to_dict()  # Accede a user_type.name dentro del contexto async
            user_type_name = user.user_type.name if user.user_type else None
            token = user_service.create_access_token({"user_id": user.id, "user_type": user_type_name})
            return user_dict, token
        # Si no existe, crear usuario (asignar un user_type_id por defecto, ej: 1)
        logging.info(f"User {email} not found. Creating new user.")
        user_in = UserCreateSchema(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=os.urandom(16).hex(),  # Contraseña aleatoria, no se usará
            user_type_id=1  # Ajustar según lógica de tu app
        )
        user = await user_service.create_user(db, user_in)
        user_dict = user.to_dict()  # Accede a user_type.name dentro del contexto async
        user_type_name = user.user_type.name if user.user_type else None
        token = user_service.create_access_token({"user_id": user.id, "user_type": user_type_name})
        logging.info(f"New user {email} created and token generated.")
        return user_dict, token 