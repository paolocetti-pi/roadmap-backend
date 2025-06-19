# Character API

A FastAPI-based REST API for managing characters and their eye colors, using Azure SQL Database for data persistence.

## Features

- CRUD operations for characters
- Eye color management
- Data validation using Pydantic
- SQLAlchemy ORM integration
- Azure SQL Database integration

## Prerequisites

- Python 3.8+
- Azure SQL Database
- ODBC Driver 17 for SQL Server

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory with your Azure SQL Database connection string:
   ```
   DATABASE_URL=mssql+pyodbc://username:password@server.database.windows.net:1433/database?driver=ODBC+Driver+17+for+SQL+Server
   ```

## Running the Application

1. Activate the virtual environment if not already activated
2. Run the application:
   ```bash
   uvicorn app:app --reload
   ```
3. Access the API documentation at `http://localhost:8000/docs`

## API Endpoints

### Characters

- `GET /character/getAll` - Get all characters
- `GET /character/get/{name}` - Get characters by name
- `POST /character/add` - Add a new character
- `DELETE /character/delete/{id}` - Delete a character by ID

### Eye Colors

- `GET /eye-colors` - Get all eye colors

## Data Models

### Character
```json
{
  "id": 1,
  "name": "Luke Skywalker",
  "height": 172,
  "mass": 77,
  "hair_color": "blond",
  "skin_color": "fair",
  "eye_color_id": 1
}
```

### Eye Color
```json
{
  "id": 1,
  "color": "blue"
}
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- 200: Success
- 400: Bad Request (invalid input or business rule violation)
- 404: Not Found
- 500: Internal Server Error 