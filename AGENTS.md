## Project Overview

This is a FastAPI application for API design enforcement. The project is built using Python 3.13+ with FastAPI, Pydantic, and Uvicorn.

## Development Commands

### Running the Application
```bash
python main.py
```
The API will be available at `http://localhost:8000` with:
- Swagger UI documentation at `/docs`
- ReDoc documentation at `/redoc`
- OpenAPI 3.1 spec at `/openapi.json`

### Package Management
This project uses `uv` for dependency management (evidenced by `uv.lock` file). Install dependencies with:
```bash
uv sync
```

## Code Architecture

### Main Application Structure
- `main.py`: Contains the complete FastAPI application with:
  - FastAPI app instance configured for OpenAPI 3.1
  - Pydantic models (`Item`, `ItemCreate`) for data validation
  - In-memory storage (`items_db` list)
  - Full CRUD API endpoints for items resource
  - Error handling with proper HTTP status codes

### API Design
The application follows RESTful conventions with:
- Resource-based URLs (`/items`, `/items/{item_id}`)
- Proper HTTP methods (GET, POST, PUT, DELETE)
- Status codes (200, 201, 404)
- Request/response models using Pydantic
- Comprehensive endpoint documentation

### Data Models
- `Item`: Complete item representation with optional ID
- `ItemCreate`: Input model for creating/updating items (excludes ID)

The application uses OpenAPI 3.1 specification and includes comprehensive API documentation accessible through the built-in Swagger UI.