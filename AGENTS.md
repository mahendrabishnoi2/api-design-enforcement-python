## Project Overview

This is a FastAPI application for API design enforcement. The project is built using Python 3.13+ with FastAPI, Pydantic, and Uvicorn.

## Development Commands

### Setup
```bash
make dev          # Install all dependencies including dev tools
make install      # Install production dependencies only
```

### Running the Application
```bash
make serve        # Start development server with auto-reload
python main.py    # Alternative: start server directly
```
The API will be available at `http://localhost:8000` with:
- Swagger UI documentation at `/docs`
- ReDoc documentation at `/redoc`
- OpenAPI 3.1 spec at `/openapi.json`

### Code Quality
```bash
make lint         # Run ruff and black linting
make format       # Auto-format code with ruff and black
make test         # Run pytest test suite
```

### API Design Enforcement
```bash
make api-lint     # Lint API design with Spectral (requires Node.js)
```

### Build and CI
```bash
make build        # Validate application builds
make ci           # Run complete CI pipeline locally
make clean        # Clean up generated files
```

### Package Management
This project uses `uv` for dependency management. The Makefile commands handle this automatically.

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

## API Design Enforcement

### Spectral Configuration
- `.spectral.yml`: Defines API design rules and style guidelines
- Extends `@stoplight/spectral-oai:recommended` for OpenAPI best practices
- Custom rules for naming conventions, HTTP status codes, and documentation requirements
- Enforces RESTful design patterns and consistent API structure

### GitHub Actions CI/CD
- Automated linting with ruff and black
- API design validation with Spectral
- Pytest test execution
- Build validation and endpoint testing
- Runs on push to main/develop branches and pull requests
- PR-specific features:
  - Runs on PR events: opened, synchronize, reopened, ready_for_review
  - Skips draft PRs automatically
  - Enhanced error reporting with GitHub annotations
  - Tests new categories API endpoints
  - Proper permissions for PR comments and checks