# Task Management API

A FastAPI-based task management system with role-based access control, similar to JIRA.

## Features

- User authentication with JWT tokens
- Role-based access control (Admin and User roles)
- Task management with status tracking
- Task comments and status history
- SQL database with SQLAlchemy ORM
- Azure SQL Database integration
- Clean Architecture implementation

## Project Structure

```
.
├── app.py                 # Main application file
├── requirements.txt       # Project dependencies
├── .env                  # Environment variables (create this file)
├── models/               # Database models
│   ├── database.py      # Database configuration
│   └── models.py        # SQLAlchemy models
├── schemas/             # Pydantic schemas
│   └── schemas.py       # Data validation schemas
├── services/            # Business logic
│   ├── auth.py         # Authentication service
│   ├── users.py        # User management service
│   └── tasks.py        # Task management service
└── routes/             # API routes
    ├── auth.py         # Authentication routes
    ├── users.py        # User management routes
    └── tasks.py        # Task management routes
```

## Database Schema

### Users Table
- id (Primary Key)
- username (Unique)
- email (Unique)
- hashed_password
- role (ADMIN/USER)
- created_at
- updated_at

### Tasks Table
- id (Primary Key)
- code (Unique)
- title
- description
- status (PENDING/IN_PROGRESS/COMPLETED/CANCELLED)
- due_date
- assigned_user_id (Foreign Key to Users)
- created_at
- updated_at

### Task Comments Table
- id (Primary Key)
- task_id (Foreign Key to Tasks)
- user_id (Foreign Key to Users)
- comment
- created_at

### Task Status History Table
- id (Primary Key)
- task_id (Foreign Key to Tasks)
- from_status
- to_status
- changed_at

## Task Status Flow

```
PENDING -> IN_PROGRESS -> COMPLETED
        \-> CANCELLED
```

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with the following variables:
```
DATABASE_URL=your_azure_sql_connection_string
SECRET_KEY=your_jwt_secret_key
```

4. Initialize the database:
```bash
# Create tables
from models.database import engine
from models.models import Base
Base.metadata.create_all(bind=engine)
```

5. Run the application:
```bash
uvicorn app:app --reload
```

## API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- POST /api/token - Get access token
- GET /api/me - Get current user info

### Users (Admin only)
- POST /api/users - Create new user
- GET /api/users - Get all users
- GET /api/users/{user_id} - Get specific user
- PUT /api/users/{user_id} - Update user
- DELETE /api/users/{user_id} - Delete user

### Tasks
- POST /api/tasks - Create new task (Admin only)
- GET /api/tasks - Get all tasks (Admin only)
- GET /api/tasks/completed - Get completed tasks (Admin only)
- GET /api/tasks/my-tasks - Get user's tasks
- GET /api/tasks/my-tasks/pending - Get user's pending tasks
- GET /api/tasks/{task_id} - Get specific task
- PUT /api/tasks/{task_id} - Update task (Admin only)
- DELETE /api/tasks/{task_id} - Delete task (Admin only)
- PUT /api/tasks/{task_id}/status/{new_status} - Change task status
- POST /api/tasks/{task_id}/comments - Add task comment
- GET /api/tasks/{task_id}/comments - Get task comments
- GET /api/tasks/{task_id}/status-history - Get task status history (Admin only)

## Development

The project follows Clean Architecture principles and uses:
- FastAPI for the web framework
- SQLAlchemy for database ORM
- Pydantic for data validation
- JWT for authentication
- Azure SQL Database for data storage

## Deployment

The application is designed to be deployed to Azure Web App Service. Make sure to:
1. Set up the required environment variables in Azure
2. Configure the Azure SQL Database connection
3. Set up proper CORS settings if needed
4. Configure proper authentication and authorization in Azure 