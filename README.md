# API de Personajes de Star Wars - Refactorización OOP (Simplificada)

Este proyecto demuestra la implementación de principios de Programación Orientada a Objetos (OOP) en una aplicación FastAPI para gestionar personajes de Star Wars. El código ha sido refactorizado de un enfoque funcional a una arquitectura OOP simplificada, fácil de entender y mantener.

## 🏗️ Resumen de la Arquitectura

La aplicación sigue una arquitectura por capas con clara separación de responsabilidades:

```
├── models/          # Modelos de datos con herencia
├── services/        # Lógica de negocio con clases base
├── routes/          # Endpoints de la API con clases router
├── schemas/         # Modelos Pydantic para validación
└── app.py           # Clase principal de la aplicación
```

## 🎯 Principios OOP Implementados (Simplificado)

### 1. **Encapsulamiento**
- Validación de datos dentro de las clases
- Acceso controlado al estado de los objetos
- Lógica de negocio encapsulada en servicios

### 2. **Herencia**
- Clase `BaseModel` para todos los modelos de base de datos
- Clase `BaseService` para operaciones CRUD comunes
- Clase `BaseRouter` para funcionalidad común de rutas

### 3. **Polimorfismo**
- Servicios que funcionan con diferentes tipos de modelos
- Métodos que pueden ser sobrescritos por subclases
- Interfaces comunes a través de clases base

### 4. **Abstracción**
- Clases base que definen funcionalidad común
- Detalles de implementación ocultos
- Interfaces públicas limpias

## 📁 Estructura del Proyecto

### Modelos (`models/`)

#### `BaseModel` (Clase Base)
```python
class BaseModel(Base):
    """Clase base de modelo con funcionalidad común"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    
    def to_dict(self) -> dict:
        """Convierte la instancia del modelo a diccionario"""
        return {
            "id": self.id
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea una instancia del modelo desde un diccionario"""
        return cls()
```

#### Clases de Modelo Concretas
- `Character`: Hereda de `BaseModel`, representa personajes de Star Wars
- `EyeColor`: Hereda de `BaseModel`, representa colores de ojos
- `KeyPhrase`: Hereda de `BaseModel`, representa frases de personajes

### Servicios (`services/`)

#### `BaseService` (Clase Base)
```python
class BaseService:
    """Clase base de servicio con operaciones CRUD comunes"""
    
    def __init__(self, model_class):
        self.model_class = model_class
    
    def get_all(self, db: Session) -> List[Dict[str, Any]]:
        """Obtiene todos los registros de la base de datos"""
        records = db.query(self.model_class).all()
        return [record.to_dict() for record in records]
    
    def create(self, db: Session, data: dict) -> Dict[str, Any]:
        """Crea un nuevo registro"""
        record = self.model_class.from_dict(data)
        db.add(record)
        db.commit()
        return record.to_dict()
    
    def validate_data(self, data: dict) -> bool:
        """Valida datos - para ser sobrescrito por subclases"""
        return True
```

#### Clases de Servicio Concretas
- `CharacterService`: Gestiona operaciones de personajes
- `EyeColorService`: Gestiona operaciones de colores de ojos
- `KeyphraseService`: Gestiona operaciones de frases clave
- `DatabaseService`: Gestiona conexiones a la base de datos

### Rutas (`routes/`)

#### `BaseRouter` (Clase Base)
```python
class BaseRouter:
    """Clase base de router con funcionalidad común"""
    
    def __init__(self, prefix: str, tags: List[str]):
        self.router = APIRouter(prefix=prefix, tags=tags)
        self.setup_routes()
    
    def setup_routes(self):
        """Configura todas las rutas - para ser sobrescrito por subclases"""
        pass
    
    def handle_exception(self, e: Exception) -> HTTPException:
        """Maneja excepciones y retorna respuestas HTTP apropiadas"""
        if isinstance(e, HTTPException):
            return e
        else:
            return HTTPException(status_code=500, detail=str(e))
```

#### Clases Router Concretas
- `CharacterRouter`: Maneja endpoints de personajes
- `EyeColorRouter`: Maneja endpoints de colores de ojos
- `KeyphraseRouter`: Maneja endpoints de frases clave

### Esquemas (`schemas/`)
- Modelos Pydantic para validación de requests/responses
- Validación de campos con restricciones
- Separación clara entre esquemas de creación, actualización y respuesta

## 🚀 Funcionalidades Clave

### 1. **Operaciones CRUD Simples**
Todos los servicios heredan de `BaseService` que provee:
- `get_all()`: Obtener todos los registros
- `get_by_id()`: Obtener por ID
- `create()`: Crear nuevos registros
- `update()`: Actualizar registros existentes
- `delete()`: Eliminar registros

### 2. **Validación de Datos**
- Validación a nivel de modelo con `to_dict()` y `from_dict()`
- Validación a nivel de servicio con reglas de negocio específicas
- Validación a nivel de esquema con Pydantic

### 3. **Manejo de Errores**
- Manejo centralizado de excepciones en clases base
- Códigos de estado HTTP apropiados
- Mensajes de error detallados

### 4. **Gestión de Base de Datos**
- Pooling de conexiones
- Manejo de transacciones
- Health checks
- Limpieza automática

## 🔧 Ejemplos de Uso

### Crear un Personaje
```python
# A nivel de servicio
character_service = CharacterService()
character_data = {
    "name": "Luke Skywalker",
    "height": 172,
    "mass": 77,
    "hair_color": "blond",
    "skin_color": "fair",
    "eye_color_id": 1
}
character = character_service.create_character(db, character_data)
```

### Agregar Rutas
```python
class CustomRouter(BaseRouter):
    def setup_routes(self):
        self.router.add_api_route(
            "/custom",
            self.custom_endpoint,
            methods=["GET"]
        )
    
    def custom_endpoint(self):
        return {"message": "Custom endpoint"}
```

## 🧪 Pruebas de la API

### Iniciar la Aplicación
```bash
python app.py
```

### Endpoints Disponibles

#### Personajes
- `GET /character/getAll` - Obtener todos los personajes
- `GET /character/get/{name}` - Obtener personajes por nombre
- `POST /character/add` - Crear un nuevo personaje
- `PUT /character/update/{id}` - Actualizar un personaje
- `DELETE /character/delete/{id}` - Eliminar un personaje
- `GET /character/{id}/phrases` - Obtener personaje con frases

#### Colores de Ojos
- `GET /eye-color/getAll` - Obtener todos los colores de ojos
- `GET /eye-color/get/{id}` - Obtener color de ojos por ID
- `POST /eye-color/add` - Crear un nuevo color de ojos
- `PUT /eye-color/update/{id}` - Actualizar un color de ojos
- `DELETE /eye-color/delete/{id}` - Eliminar un color de ojos

#### Frases Clave
- `GET /keyphrases?text=...` - Extraer frases clave usando Azure
- `POST /keyphrases/{character_id}` - Extraer y guardar frases clave para un personaje
- `GET /keyphrases/{character_id}` - Obtener frases clave de un personaje específico

### Health Check
- `GET /health` - Verificar salud de la API y la base de datos

## 📊 Beneficios del Refactor OOP Simplificado

1. **Reutilización de Código**: Funcionalidad común en clases base
2. **Mantenibilidad**: Separación clara de responsabilidades
3. **Extensibilidad**: Fácil de agregar nuevos modelos, servicios y rutas
4. **Consistencia**: Patrones estandarizados en toda la aplicación
5. **Testing**: Más fácil de testear componentes individuales
6. **Documentación**: Estructura de código auto-documentada
7. **Accesibilidad**: Fácil de entender y modificar

## 🔄 Qué se Simplificó

El refactor eliminó características complejas para hacer el código más accesible:

1. **Sin ABC (Clases Abstractas)**: No más decoradores `@abstractmethod`
2. **Sin Tipos Genéricos**: No más `Generic[T]` o `TypeVar('T')`
3. **Herencia Simplificada**: Herencia regular en vez de clases abstractas
4. **Principios OOP Clave**: Herencia, encapsulamiento, polimorfismo y abstracción

## 🛠️ Dependencias

- FastAPI
- SQLAlchemy
- Pydantic
- Python-dotenv
- Uvicorn

## 📝 Variables de Entorno

Crea un archivo `.env` con:
```
DATABASE_URL=sqlite:///./star_wars.db
AZURE_LANGUAGE_ENDPOINT=tu_endpoint_azure
AZURE_LANGUAGE_KEY=tu_clave_azure
```

## 🎯 ¿Por qué este enfoque?

Este enfoque OOP simplificado provee:

- **Aprendizaje más fácil**: Sin teoría de tipos compleja ni conceptos abstractos
- **Mejor mantenibilidad**: Herencia y sobreescritura de métodos directa
- **Desarrollo más rápido**: Menos código repetitivo
- **Apto para equipos**: Accesible para desarrolladores de todos los niveles
- **Sigue siendo OOP**: Mantiene todos los principios OOP sin complejidad

El código refactorizado demuestra cómo los principios OOP pueden aplicarse efectivamente para crear una API más mantenible, extensible y robusta sin complejidad innecesaria.

## CI/CD con GitHub Actions y Azure Web App

Este proyecto utiliza GitHub Actions para automatizar la integración y el despliegue continuo (CI/CD) hacia una Azure Web App.

**Pasos principales:**
1. Cada vez que se hace push a la rama `main`, se ejecuta el workflow.
2. El workflow instala dependencias y despliega el código a Azure Web App usando el *publish profile* almacenado como secreto.
3. El despliegue es automático y no requiere intervención manual.

**Configuración:**
- El *publish profile* de Azure se almacena como secreto en GitHub bajo el nombre `AZUREAPPSERVICE_PUBLISHPROFILE`.
- El workflow se encuentra en `.github/workflows/azure-webapp.yml`.
- Cuando crees tu Azure Web App, reemplaza `TU_WEBAPP_AQUI` en el archivo de workflow por el nombre real de tu Web App.

**Referencias útiles:**
- [Docs Azure Web Apps Deploy Action](https://github.com/Azure/webapps-deploy)
- [Más GitHub Actions para Azure](https://github.com/Azure/actions)
- [Python, GitHub Actions y Azure App Service](https://aka.ms/python-webapps-actions)

## 🔐 Autenticación y Autorización JWT

### Registro y Login de Usuarios

- **Registro:**
  - Endpoint: `POST /users/register`
  - Permite registrar un nuevo usuario enviando: nombre, apellido, email, contraseña y tipo de usuario (debe existir el tipo, por ejemplo: `ADMIN` o `USER`).
  - Ejemplo de body:
    ```json
    {
      "first_name": "Luke",
      "last_name": "Skywalker",
      "email": "luke@jedi.com",
      "password": "123456",
      "user_type_id": 1
    }
    ```

- **Login:**
  - Endpoint: `POST /users/login`
  - Utiliza el estándar OAuth2PasswordRequestForm, por lo que el campo `username` debe contener el email del usuario.
  - Ejemplo de body (x-www-form-urlencoded):
    ```
    username=luke@jedi.com
    password=123456
    ```
  - Devuelve un JWT en el campo `access_token`.

### Uso del JWT en Swagger

1. Haz login en `/users/login` y copia el `access_token`.
2. Haz clic en el botón **Authorize** de Swagger y pega el token como:
   ```
   Bearer <access_token>
   ```
3. Ahora puedes acceder a las rutas protegidas.

### Protección de Rutas

- **[GET]** Todas las rutas requieren un JWT válido (usuario autenticado).
- **[POST], [PUT], [DELETE]** Solo pueden ser accedidas por usuarios con tipo `ADMIN`.
- Si el token es inválido o expirado, se devuelve 401.
- Si el usuario no es admin y accede a rutas restringidas, se devuelve 403.

### Ejemplo de flujo de autenticación

1. Registrar usuario (POST /users/register)
2. Login (POST /users/login) → obtener access_token
3. Usar el token en Swagger o en tus requests:
   ```http
   Authorization: Bearer <access_token>
   ```

### Notas importantes
- El campo `username` en el login es el email del usuario.
- Los tipos de usuario válidos deben existir en la tabla `user_types` (`ADMIN`, `USER`).
- El token JWT contiene el id, email y tipo de usuario.
- El backend utiliza PyJWT y passlib para la seguridad, siguiendo las recomendaciones oficiales de FastAPI.

---

## 🔑 Single Sign-On (SSO) con Google y Microsoft

### Prerrequisitos
- Tener una cuenta en Google Cloud Platform y en Azure Portal (Microsoft Entra ID).
- Registrar tu aplicación en ambos proveedores para obtener los CLIENT_ID y CLIENT_SECRET.

### Variables de entorno necesarias
Agrega a tu `.env`:
```
GOOGLE_CLIENT_ID=tu_client_id_google
GOOGLE_CLIENT_SECRET=tu_client_secret_google
GOOGLE_REDIRECT_URI=http://localhost:8000/sso/auth/google/callback
MICROSOFT_CLIENT_ID=tu_client_id_microsoft
MICROSOFT_CLIENT_SECRET=tu_client_secret_microsoft
MICROSOFT_REDIRECT_URI=http://localhost:8000/sso/auth/microsoft/callback
MICROSOFT_TENANT_ID=common  # O déjalo vacío para aceptar cualquier cuenta
```

### Configuración en Google Cloud Platform
1. Ve a [Google Cloud Console](https://console.cloud.google.com/apis/credentials).
2. Crea un nuevo OAuth 2.0 Client ID.
3. Agrega el URI de redirección: `http://localhost:8000/sso/auth/google/callback`.
4. Copia el CLIENT_ID y CLIENT_SECRET y colócalos en tu `.env`.

### Configuración en Azure Portal (Microsoft Entra ID)
1. Ve a [Azure Portal](https://portal.azure.com) → Azure Active Directory → Registros de aplicaciones.
2. Registra una nueva aplicación.
3. En "Tipos de cuenta admitidos" selecciona:
   - **Cuentas en cualquier directorio organizativo y cuentas personales de Microsoft (por ejemplo, Skype, Xbox)**
4. Agrega el URI de redirección: `http://localhost:8000/sso/auth/microsoft/callback`.
5. Copia el CLIENT_ID y CLIENT_SECRET y colócalos en tu `.env`.
6. Si quieres aceptar cualquier cuenta, pon `MICROSOFT_TENANT_ID=common` o deja la variable vacía.

#### ⚠️ Problema común con Microsoft
Si ves el error:
```
The request is not valid for the application's 'userAudience' configuration. In order to use /common/ endpoint, the application must not be configured with 'Consumer' as the user audience. The userAudience should be configured with 'All' to use /common/ endpoint.
```
Debes cambiar la opción de "Tipos de cuenta admitidos" a **All** (ver paso 3 arriba).

### Endpoints SSO disponibles
- `GET /sso/login/google` → Redirige a Google para autenticación
- `GET /sso/auth/google/callback` → Callback de Google (no la llames manualmente)
- `GET /sso/login/microsoft` → Redirige a Microsoft para autenticación
- `GET /sso/auth/microsoft/callback` → Callback de Microsoft (no la llames manualmente)

### Flujo de autenticación SSO
1. El usuario accede a `/sso/login/google` o `/sso/login/microsoft`.
2. Se redirige al proveedor para autorizar la app.
3. El proveedor redirige a tu backend con un código de autorización.
4. El backend intercambia el código por un token y obtiene la información del usuario.
5. Si el usuario ya existe, se le genera un JWT; si no, se registra automáticamente.

### Notas adicionales
- El campo `user_type_id` para usuarios SSO se asigna por defecto a `1` (ajusta según tu lógica).
- El backend maneja la creación y login de usuarios SSO de forma transparente.
- Puedes usar el JWT devuelto para autenticarte en las rutas protegidas igual que con el login tradicional.

## 🐳 Dockerización y Despliegue

### 1. **Requisitos previos**
- Tener instalado [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/install/).

---

### 2. **Construcción y ejecución con Docker Compose**

```bash
docker-compose up --build
```

- Esto levantará:
  - La API FastAPI en [http://localhost:8000/](http://localhost:8000/)
  - MySQL en el puerto 3306 (solo accesible internamente)
  - phpMyAdmin en [http://localhost:8080/](http://localhost:8080/) para gestionar la base de datos visualmente

---

### 3. **Acceso a phpMyAdmin**

- URL: [http://localhost:8080/](http://localhost:8080/)
- Usuario: `myuser`
- Contraseña: `mypassword`
- Servidor: `db`

---

### 4. **Persistencia y logs**

- **Datos de la base de datos**: Se almacenan en el volumen `mysql_data` y persisten aunque detengas los contenedores.
- **Logs de la API**: Se almacenan en `./logs/api/app.log` (en tu máquina local).
- **Logs de MySQL**: Se almacenan en `./logs/mysql/` (en tu máquina local).

---

### 5. **Variables de entorno**

Puedes definir variables de entorno en un archivo `.env` en la raíz del proyecto y Docker Compose las cargará automáticamente.

---

### 6. **Red interna automática**

Docker Compose crea una red interna para que los servicios se comuniquen usando el nombre del servicio como hostname (por ejemplo, la API se conecta a la base de datos usando `db` como host).

---

### 7. **Comandos útiles**

- **Levantar en segundo plano:**  
  `docker-compose up -d --build`
- **Ver logs de todos los servicios:**  
  `docker-compose logs -f`
- **Detener y eliminar contenedores:**  
  `docker-compose down`
- **Reconstruir solo la API:**  
  `docker-compose build api`

---

### 8. **Notas adicionales**

- Si quieres habilitar logs generales de MySQL, puedes agregar un archivo `my.cnf` personalizado.
- La carpeta `logs/` debe existir o será creada automáticamente por la app/API. 