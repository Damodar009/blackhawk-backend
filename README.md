# Blackhawk Backend

Production-ready Python backend for Blackhawk using FastAPI, Poetry, Docker, and SQLAlchemy.

## Features

- **FastAPI**: High performance, easy to learn, fast to code, ready for production.
- **Poetry**: Dependency management and packaging made easy.
- **Docker**: Containerized application for consistent environments.
- **SQLAlchemy 2.0**: Modern ORM for database interactions.
- **Alembic**: Database migrations.
- **LangChain**: AI integration for LLM workflows.
- **PostgreSQL**: Robust relational database.

## Setup

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Poetry (optional, for local dev)

### Local Development

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    # OR with Poetry
    poetry install
    ```

2.  **Environment Variables**:
    Copy `.env.example` to `.env` and update values.
    ```bash
    cp .env.example .env
    ```

3.  **Run Database**:
    You can use Docker to run just the database:
    ```bash
    docker-compose -f docker/docker-compose.yml up -d db
    ```

4.  **Run Migrations**:
    ```bash
    alembic upgrade head
    ```

5.  **Run Application**:
    ```bash
    uvicorn app.main:app --reload
    ```
    Access API documentation at `http://localhost:8000/docs`.

### Docker

Run the entire stack with Docker Compose:

```bash
make docker-up
```

This will start the backend and database services.

## Project Structure

- `app/`: Main application code.
    - `api/`: API endpoints and routers.
    - `core/`: Configuration and logging.
    - `db/`: Database session and base models.
    - `models/`: SQLAlchemy models.
    - `schemas/`: Pydantic schemas.
    - `services/`: Business logic.
- `alembic/`: Database migrations.
- `docker/`: Docker configuration.
- `tests/`: Tests.

## API Usage

### Health Check
`GET /api/v1/health`

### Users
`POST /api/v1/users/` - Create user
`GET /api/v1/users/{id}` - Get user

### AI Chat
`POST /api/v1/ai/test` - Test LangChain integration

## Testing

Run tests with:
```bash
make test
```
