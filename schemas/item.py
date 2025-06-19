from pydantic import BaseModel, Field
from typing import Optional

class Item(BaseModel):
    id: int
    name: str
    height: int
    mass: int
    hair_color: str
    skin_color: str
    eye_color: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Luke Skywalker",
                "height": 172,
                "mass": 77,
                "hair_color": "blond",
                "skin_color": "fair",
                "eye_color": "blue"
            }
        } 