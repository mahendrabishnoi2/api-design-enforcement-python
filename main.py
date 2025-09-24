import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="API Design Enforcement",
    description="A FastAPI application with OpenAPI 3.1 support",
    version="0.1.0",
    openapi_version="3.1.0",
)


class Item(BaseModel):
    id: int | None = None
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    category_id: int | None = None


class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    category_id: int | None = None


class Category(BaseModel):
    id: int | None = None
    name: str
    description: str | None = None


class CategoryCreate(BaseModel):
    name: str
    description: str | None = None


items_db = []
categories_db = []


@app.get("/")
async def root():
    """Root endpoint returning a welcome message."""
    return {"message": "Welcome to API Design Enforcement API"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/items", response_model=list[Item])
async def get_items():
    """Get all items."""
    return items_db


@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Get a specific item by ID."""
    for item in items_db:
        if item.get("id") == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/items", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    """Create a new item."""
    new_item = item.model_dump()
    new_item["id"] = len(items_db) + 1
    items_db.append(new_item)
    return new_item


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemCreate):
    """Update an existing item."""
    for i, existing_item in enumerate(items_db):
        if existing_item.get("id") == item_id:
            updated_item = item.model_dump()
            updated_item["id"] = item_id
            items_db[i] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """Delete an item."""
    for i, item in enumerate(items_db):
        if item.get("id") == item_id:
            items_db.pop(i)
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/categories", response_model=list[Category])
async def get_categories():
    """Get all categories."""
    return categories_db


@app.get("/categories/{category_id}", response_model=Category)
async def get_category(category_id: int):
    """Get a specific category by ID."""
    for category in categories_db:
        if category.get("id") == category_id:
            return category
    raise HTTPException(status_code=404, detail="Category not found")


@app.post("/categories", response_model=Category, status_code=201)
async def create_category(category: CategoryCreate):
    """Create a new category."""
    new_category = category.model_dump()
    new_category["id"] = len(categories_db) + 1
    categories_db.append(new_category)
    return new_category


@app.put("/categories/{category_id}", response_model=Category)
async def update_category(category_id: int, category: CategoryCreate):
    """Update an existing category."""
    for i, existing_category in enumerate(categories_db):
        if existing_category.get("id") == category_id:
            updated_category = category.model_dump()
            updated_category["id"] = category_id
            categories_db[i] = updated_category
            return updated_category
    raise HTTPException(status_code=404, detail="Category not found")


@app.delete("/categories/{category_id}")
async def delete_category(category_id: int):
    """Delete a category."""
    for i, category in enumerate(categories_db):
        if category.get("id") == category_id:
            categories_db.pop(i)
            return {"message": "Category deleted successfully"}
    raise HTTPException(status_code=404, detail="Category not found")


@app.get("/categories/{category_id}/items", response_model=list[Item])
async def get_items_by_category(category_id: int):
    """Get all items in a specific category."""
    # First check if category exists
    category_exists = any(cat.get("id") == category_id for cat in categories_db)
    if not category_exists:
        raise HTTPException(status_code=404, detail="Category not found")

    # Return items that belong to this category
    return [item for item in items_db if item.get("category_id") == category_id]


# BAD API DESIGN EXAMPLES - These will trigger Spectral errors/warnings


@app.get("/api/v1/get-all-items")  # Violates: HTTP verbs in path, not kebab-case
async def get_all_items_bad():
    """This endpoint violates multiple API design rules."""
    return items_db


@app.post("/createNewCategory")  # Violates: HTTP verbs in path, camelCase
async def create_new_category_bad():
    """Another bad endpoint design."""
    return {"message": "This is poorly designed"}


@app.get("/items/search_by_name")  # Violates: snake_case instead of kebab-case
async def search_items_by_name_bad():
    """Search items - but with bad URL design."""
    return []


@app.delete("/admin/deleteEverything")  # Violates: camelCase, HTTP verb in path
async def admin_delete_everything():
    """Dangerous endpoint with poor naming."""
    return {"message": "Everything deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
