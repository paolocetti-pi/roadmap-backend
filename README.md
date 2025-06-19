# Star Wars Characters API

A FastAPI-based REST API for managing Star Wars character data.

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

## Available Endpoints

- `GET /items/getAll`: Get all items
- `GET /items/get/{name}`: Get items by name
- `POST /items/add`: Add a new item
- `DELETE /items/delete/{id}`: Delete an item by id

## Data Structure

Each item has the following structure:
```json
{
    "id": 1,
    "name": "Luke Skywalker",
    "height": 172,
    "mass": 77,
    "hair_color": "blond",
    "skin_color": "fair",
    "eye_color": "blue"
}
``` 