from typing import List, Optional
from schemas.item import Item

# Sample data
items = [
    {
        "id": 1,
        "name": "Luke Skywalker",
        "height": 172,
        "mass": 77,
        "hair_color": "blond",
        "skin_color": "fair",
        "eye_color": "blue"
    },
    {
        "id": 2,
        "name": "R2-D2",
        "height": 96,
        "mass": 32,
        "hair_color": "n/a",
        "skin_color": "blue",
        "eye_color": "red"
    },
    {
        "id": 3,
        "name": "C-3PO",
        "height": 167,
        "mass": 75,
        "hair_color": "n/a",
        "skin_color": "gold",
        "eye_color": "yellow"
    },
    {
        "id": 4,
        "name": "Darth Vader",
        "height": 202,
        "mass": 136,
        "hair_color": "none",
        "skin_color": "white",
        "eye_color": "yellow"
    },
    {
        "id": 5,
        "name": "Leia Organa",
        "height": 150,
        "mass": 49,
        "hair_color": "brown",
        "skin_color": "light",
        "eye_color": "brown"
    },
    {
        "id": 6,
        "name": "Owen Lars",
        "height": 178,
        "mass": 120,
        "hair_color": "grey",
        "skin_color": "light",
        "eye_color": "blue"
    },
    {
        "id": 7,
        "name": "Beru Whitesun lars",
        "height": 165,
        "mass": 75,
        "hair_color": "brown",
        "skin_color": "light",
        "eye_color": "blue"
    },
    {
        "id": 8,
        "name": "R5-D4",
        "height": 97,
        "mass": 32,
        "hair_color": "n/a",
        "skin_color": "white",
        "eye_color": "red"
    }
]

def get_all_items() -> List[Item]:
    """Get all items"""
    return [Item(**item) for item in items]

def get_item_by_name(name: str) -> List[Item]:
    """Get items by name"""
    return [Item(**item) for item in items if item["name"].lower() == name.lower()]

def add_item(item: Item) -> Item:
    """Add a new item"""
    # Check if item with same id exists
    if any(existing_item["id"] == item.id for existing_item in items):
        raise ValueError(f"Item with id {item.id} already exists")
    
    new_item = item.dict()
    items.append(new_item)
    return item

def delete_item(item_id: int) -> bool:
    """Delete an item by id"""
    for i, item in enumerate(items):
        if item["id"] == item_id:
            items.pop(i)
            return True
    return False 