# Star Wars Characters API - OOP Refactoring (Simplified)

This project demonstrates the implementation of Object-Oriented Programming (OOP) principles in a FastAPI application for managing Star Wars characters. The code has been refactored from a functional approach to a simplified OOP architecture that's easy to understand and maintain.

## 🏗️ Architecture Overview

The application follows a layered architecture with clear separation of concerns:

```
├── models/          # Data models with inheritance
├── services/        # Business logic with base classes
├── routes/          # API endpoints with router classes
├── schemas/         # Pydantic models for validation
└── app.py          # Main application class
```

## 🎯 OOP Principles Implemented (Simplified)

### 1. **Encapsulation**
- Data validation within classes
- Controlled access to object state
- Business logic encapsulated in services

### 2. **Inheritance**
- `BaseModel` class for all database models
- `BaseService` class for common CRUD operations
- `BaseRouter` class for common routing functionality

### 3. **Polymorphism**
- Services that work with different model types
- Methods that can be overridden by subclasses
- Common interfaces through base classes

### 4. **Abstraction**
- Base classes defining common functionality
- Hidden implementation details
- Clean public interfaces

## 📁 Project Structure

### Models (`models/`)

#### `BaseModel` (Base Class)
```python
class BaseModel(Base):
    """Base model class with common functionality"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary"""
        return {
            "id": self.id
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create model instance from dictionary"""
        return cls()
```

#### Concrete Model Classes
- `Character`: Inherits from `BaseModel`, represents Star Wars characters
- `EyeColor`: Inherits from `BaseModel`, represents eye colors
- `KeyPhrase`: Inherits from `BaseModel`, represents character phrases

### Services (`services/`)

#### `BaseService` (Base Class)
```python
class BaseService:
    """Base service class with common CRUD operations"""
    
    def __init__(self, model_class):
        self.model_class = model_class
    
    def get_all(self, db: Session) -> List[Dict[str, Any]]:
        """Get all records from the database"""
        records = db.query(self.model_class).all()
        return [record.to_dict() for record in records]
    
    def create(self, db: Session, data: dict) -> Dict[str, Any]:
        """Create a new record"""
        record = self.model_class.from_dict(data)
        db.add(record)
        db.commit()
        return record.to_dict()
    
    def validate_data(self, data: dict) -> bool:
        """Validate data - to be overridden by subclasses"""
        return True
```

#### Concrete Service Classes
- `CharacterService`: Manages character operations
- `EyeColorService`: Manages eye color operations
- `KeyphraseService`: Manages key phrase operations
- `DatabaseService`: Manages database connections

### Routes (`routes/`)

#### `BaseRouter` (Base Class)
```python
class BaseRouter:
    """Base router class with common functionality"""
    
    def __init__(self, prefix: str, tags: List[str]):
        self.router = APIRouter(prefix=prefix, tags=tags)
        self.setup_routes()
    
    def setup_routes(self):
        """Setup all routes - to be overridden by subclasses"""
        pass
    
    def handle_exception(self, e: Exception) -> HTTPException:
        """Handle exceptions and return appropriate HTTP responses"""
        if isinstance(e, HTTPException):
            return e
        else:
            return HTTPException(status_code=500, detail=str(e))
```

#### Concrete Router Classes
- `CharacterRouter`: Handles character endpoints
- `EyeColorRouter`: Handles eye color endpoints
- `KeyphraseRouter`: Handles key phrase endpoints

### Schemas (`schemas/`)
- Pydantic models for request/response validation
- Proper field validation with constraints
- Clear separation between create, update, and response schemas

## 🚀 Key Features

### 1. **Simple CRUD Operations**
All services inherit from `BaseService` which provides:
- `get_all()`: Retrieve all records
- `get_by_id()`: Retrieve by ID
- `create()`: Create new records
- `update()`: Update existing records
- `delete()`: Delete records

### 2. **Data Validation**
- Model-level validation through `to_dict()` and `from_dict()` methods
- Service-level validation with specific business rules
- Schema-level validation with Pydantic

### 3. **Error Handling**
- Centralized exception handling in base classes
- Proper HTTP status codes
- Detailed error messages

### 4. **Database Management**
- Connection pooling
- Transaction management
- Health checks
- Automatic cleanup

## 🔧 Usage Examples

### Creating a Character
```python
# Service level
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

### Adding Routes
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

## 🧪 Testing the API

### Start the Application
```bash
python app.py
```

### Available Endpoints

#### Characters
- `GET /character/getAll` - Get all characters
- `GET /character/get/{name}` - Get characters by name
- `POST /character/add` - Create a new character
- `PUT /character/update/{id}` - Update a character
- `DELETE /character/delete/{id}` - Delete a character
- `GET /character/{id}/phrases` - Get character with phrases

#### Eye Colors
- `GET /eye-color/getAll` - Get all eye colors
- `GET /eye-color/get/{id}` - Get eye color by ID
- `POST /eye-color/add` - Create a new eye color
- `PUT /eye-color/update/{id}` - Update an eye color
- `DELETE /eye-color/delete/{id}` - Delete an eye color

#### Key Phrases
- `GET /keyphrases?text=...` - Extract key phrases from text using Azure
- `POST /keyphrases/{character_id}` - Extract and save key phrases for a character
- `GET /keyphrases/{character_id}` - Get key phrases for a specific character

### Health Check
- `GET /health` - Check API and database health

## 📊 Benefits of Simplified OOP Refactoring

1. **Code Reusability**: Common functionality in base classes
2. **Maintainability**: Clear separation of concerns
3. **Extensibility**: Easy to add new models, services, and routes
4. **Consistency**: Standardized patterns across the application
5. **Testing**: Easier to test individual components
6. **Documentation**: Self-documenting code structure
7. **Accessibility**: Easy to understand and modify

## 🔄 What Was Simplified

The refactoring removed complex features to make the code more accessible:

1. **Removed ABC (Abstract Base Classes)**: No more `@abstractmethod` decorators
2. **Removed Generic Types**: No more `Generic[T]` or `TypeVar('T')`
3. **Simplified Inheritance**: Regular inheritance instead of abstract classes
4. **Kept Core OOP Principles**: Inheritance, encapsulation, polymorphism, and abstraction

## 🛠️ Dependencies

- FastAPI
- SQLAlchemy
- Pydantic
- Python-dotenv
- Uvicorn

## 📝 Environment Variables

Create a `.env` file with:
```
DATABASE_URL=sqlite:///./star_wars.db
AZURE_LANGUAGE_ENDPOINT=your_azure_endpoint
AZURE_LANGUAGE_KEY=your_azure_key
```

## 🎯 Why This Approach?

This simplified OOP approach provides:

- **Easier Learning**: No complex type theory or abstract concepts
- **Better Maintainability**: Straightforward inheritance and method overriding
- **Faster Development**: Less boilerplate code
- **Team-Friendly**: Accessible to developers of all skill levels
- **Still OOP**: Maintains all core OOP principles without complexity

The refactored codebase demonstrates how OOP principles can be effectively applied to create a more maintainable, extensible, and robust API application without unnecessary complexity.

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