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
