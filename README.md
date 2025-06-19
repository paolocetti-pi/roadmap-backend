# Character API

A FastAPI-based REST API for managing characters, their eye colors, and key phrases using Azure SQL Database for data persistence and Azure Cognitive Services for key phrase extraction.

## Features

- CRUD operations for characters
- Eye color management
- Key phrase extraction using Azure Cognitive Services
- Association of key phrases to characters
- Data validation using Pydantic
- SQLAlchemy ORM integration
- Azure SQL Database integration

## Prerequisites

- Python 3.8+
- Azure SQL Database
- ODBC Driver 17 for SQL Server
- Azure Cognitive Services (Language Resource)

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
4. Create a `.env` file in the root directory with your Azure SQL Database connection string and Azure Cognitive Services credentials:
   ```
   DATABASE_URL=mssql+pyodbc://username:password@server.database.windows.net:1433/database?driver=ODBC+Driver+17+for+SQL+Server
   AZURE_LANGUAGE_ENDPOINT=https://<your-resource-name>.cognitiveservices.azure.com/
   AZURE_LANGUAGE_KEY=<your-azure-key>
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

### Key Phrases (Azure Cognitive Services)

- `GET /keyphrases?text=...` - Extract key phrases from a text using Azure
- `POST /keyphrases/{character_id}` - Extract key phrases from a text and associate them to a character (body: `{ "text": "..." }`)
- `GET /keyphrases/{character_id}` - Get all key phrases associated with a character

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
  "birth_year": "19BBY",
  "eye_color": 1
}
```

### Eye Color
```json
{
  "id": 1,
  "color": "blue"
}
```

### KeyPhrase
```json
{
  "id": 1,
  "character_id": 1,
  "phrase": "Jedi Knight"
}
```

### CharacterKeyPhrasesOut
```json
{
  "id_character": 1,
  "key_phrases": ["Jedi Knight", "Rebel Alliance"]
}
```

## Azure Key Phrase Extraction

This API uses the official Azure SDK (`azure-ai-textanalytics`) to extract key phrases from text. You must provide your Azure Cognitive Services endpoint and key in the `.env` file.

For more information, see the [Azure Text Analytics client library for Python](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-textanalytics-readme?view=azure-python).

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- 200: Success
- 400: Bad Request (invalid input or business rule violation)
- 404: Not Found
- 500: Internal Server Error 