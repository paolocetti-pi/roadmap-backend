import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from app import app
from services.database import get_db
from models.base import Base
from models.character import Character
from models.eye_color import EyeColor
from routes.user_routes import get_current_user, require_admin_user

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        # Add initial data
        eye_color = EyeColor(color="Blue")
        db.add(eye_color)
        db.commit()
        db.refresh(eye_color)
        
        character1 = Character(name="Luke Skywalker", eye_color_id=eye_color.id, height=172, mass=77, hair_color="Blond", skin_color="Fair")
        character2 = Character(name="Anakin Skywalker", eye_color_id=eye_color.id, height=188, mass=84, hair_color="Blond", skin_color="Fair")
        db.add(character1)
        db.add(character2)
        db.commit()
        yield db
    finally:
        db.close()

# Mock user for authentication
mock_user = {"username": "testuser", "is_admin": True}

def get_mock_current_user():
    return mock_user

def require_mock_admin_user():
    if not mock_user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin access required")
    return mock_user

app.dependency_overrides[get_current_user] = get_mock_current_user
app.dependency_overrides[require_admin_user] = require_mock_admin_user


def test_get_all_characters(db_session):
    response = client.get("/character/getAll")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Luke Skywalker"
    assert data[1]["name"] == "Anakin Skywalker"

def test_get_all_characters_empty(db_session):
    db_session.query(Character).delete()
    db_session.commit()
    response = client.get("/character/getAll")
    assert response.status_code == 200
    assert response.json() == []

def test_get_character_by_name(db_session):
    response = client.get("/character/get/Luke Skywalker")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Luke Skywalker"

def test_get_character_by_name_not_found():
    response = client.get("/character/get/NonExistentCharacter")
    assert response.status_code == 404
    assert response.json() == {"detail": "No characters found with this name"}

def test_create_character(db_session):
    eye_color_id = db_session.query(EyeColor).first().id
    new_character = {
        "name": "Leia Organa",
        "eye_color_id": eye_color_id,
        "height": 150,
        "mass": 49,
        "hair_color": "Brown",
        "skin_color": "Light"
    }
    response = client.post("/character/add", json=new_character)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Leia Organa"
    assert "id" in data

    # Verify it was added to the db
    characters_in_db = db_session.query(Character).all()
    assert len(characters_in_db) == 3

def test_create_character_missing_fields():
    new_character = {"name": "Incomplete Character"}
    response = client.post("/character/add", json=new_character)
    assert response.status_code == 422

def test_delete_character(db_session):
    character_to_delete = db_session.query(Character).filter(Character.name == "Luke Skywalker").first()
    response = client.delete(f"/character/delete/{character_to_delete.id}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Character with id {character_to_delete.id} successfully deleted"}
    
    # Verify it was deleted from the db
    character_in_db = db_session.query(Character).filter(Character.id == character_to_delete.id).first()
    assert character_in_db is None

def test_delete_character_not_found(db_session):
    response = client.delete("/character/delete/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Character not found"}
