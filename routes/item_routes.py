from fastapi import APIRouter, HTTPException
from typing import List
from schemas.item import Item
from services.item_service import get_all_items, get_item_by_name, add_item, delete_item

router = APIRouter()

@router.get("/items/getAll", response_model=List[Item], tags=["items"])
async def get_items():
    """
    Get all items.
    
    Returns:
        List[Item]: A list of all items
    """
    return get_all_items()

@router.get("/items/get/{name}", response_model=List[Item], tags=["items"])
async def get_items_by_name(name: str):
    """
    Get items by name.
    
    Args:
        name (str): The name to search for
        
    Returns:
        List[Item]: A list of items matching the name
    """
    items = get_item_by_name(name)
    if not items:
        raise HTTPException(status_code=404, detail=f"No items found with name {name}")
    return items

@router.post("/items/add", response_model=Item, tags=["items"])
async def create_item(item: Item):
    """
    Create a new item.
    
    Args:
        item (Item): The item to create
        
    Returns:
        Item: The created item
        
    Raises:
        HTTPException: If an item with the same id already exists
    """
    try:
        return add_item(item)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/items/delete/{item_id}", tags=["items"])
async def remove_item(item_id: int):
    """
    Delete an item by id.
    
    Args:
        item_id (int): The id of the item to delete
        
    Returns:
        dict: A message indicating success
        
    Raises:
        HTTPException: If the item is not found
    """
    if delete_item(item_id):
        return {"message": f"Item with id {item_id} deleted successfully"}
    raise HTTPException(status_code=400, detail=f"Item with id {item_id} not found") 