from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to API Design Enforcement API"}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_items_empty():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_create_item():
    item_data = {
        "name": "Test Item",
        "description": "A test item",
        "price": 10.99,
        "tax": 1.10,
    }
    response = client.post("/items", json=item_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["price"] == item_data["price"]
    assert "id" in data


def test_get_item():
    # First create an item
    item_data = {
        "name": "Test Item 2",
        "description": "Another test item",
        "price": 15.99,
    }
    create_response = client.post("/items", json=item_data)
    item_id = create_response.json()["id"]

    # Then get it
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["id"] == item_id


def test_get_nonexistent_item():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_update_item():
    # Create item
    item_data = {"name": "Original Item", "price": 20.99}
    create_response = client.post("/items", json=item_data)
    item_id = create_response.json()["id"]

    # Update item
    updated_data = {
        "name": "Updated Item",
        "price": 25.99,
        "description": "Updated description",
    }
    response = client.put(f"/items/{item_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["price"] == updated_data["price"]
    assert data["id"] == item_id


def test_delete_item():
    # Create item
    item_data = {"name": "Item to Delete", "price": 5.99}
    create_response = client.post("/items", json=item_data)
    item_id = create_response.json()["id"]

    # Delete item
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted successfully"}

    # Verify item is deleted
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404


def test_openapi_spec():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert data["openapi"] == "3.1.0"
    assert data["info"]["title"] == "API Design Enforcement"


def test_get_categories_empty():
    response = client.get("/categories")
    assert response.status_code == 200
    assert response.json() == []


def test_create_category():
    category_data = {"name": "Electronics", "description": "Electronic items"}
    response = client.post("/categories", json=category_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == category_data["name"]
    assert data["description"] == category_data["description"]
    assert "id" in data


def test_get_category():
    # Create category first
    category_data = {"name": "Books", "description": "Book items"}
    create_response = client.post("/categories", json=category_data)
    category_id = create_response.json()["id"]

    # Get the category
    response = client.get(f"/categories/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == category_data["name"]
    assert data["id"] == category_id


def test_update_category():
    # Create category
    category_data = {"name": "Original Category"}
    create_response = client.post("/categories", json=category_data)
    category_id = create_response.json()["id"]

    # Update category
    updated_data = {"name": "Updated Category", "description": "Updated description"}
    response = client.put(f"/categories/{category_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["description"] == updated_data["description"]


def test_delete_category():
    # Create category
    category_data = {"name": "Category to Delete"}
    create_response = client.post("/categories", json=category_data)
    category_id = create_response.json()["id"]

    # Delete category
    response = client.delete(f"/categories/{category_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Category deleted successfully"}

    # Verify deletion
    get_response = client.get(f"/categories/{category_id}")
    assert get_response.status_code == 404


def test_get_items_by_category():
    # Create category
    category_data = {"name": "Test Category"}
    cat_response = client.post("/categories", json=category_data)
    category_id = cat_response.json()["id"]

    # Create item in category
    item_data = {"name": "Test Item", "price": 10.99, "category_id": category_id}
    client.post("/items", json=item_data)

    # Get items by category
    response = client.get(f"/categories/{category_id}/items")
    assert response.status_code == 200
    items = response.json()
    assert len(items) >= 1
    assert items[0]["category_id"] == category_id


def test_get_items_by_nonexistent_category():
    response = client.get("/categories/999/items")
    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}
