# Module 11 – FastAPI Calculator and User API with PostgreSQL

## Project Overview

This project builds on my previous FastAPI application by expanding its database functionality using Python, SQLAlchemy, PostgreSQL, and Pydantic.

The application includes user management functionality and a calculation model that supports addition, subtraction, multiplication, and division. SQLAlchemy is used to interact with PostgreSQL, while Pydantic schemas validate incoming calculation data and control the information returned by the API.

This project also builds on concepts from previous modules, including database management, object-oriented programming, automated testing, Docker containerization, and continuous integration and deployment (CI/CD) using GitHub Actions.

## Technologies Used

- **Python 3.14** – Programming language.
- **FastAPI** – Web framework used to build the API.
- **SQLAlchemy** – ORM used to interact with PostgreSQL.
- **PostgreSQL 16** – Relational database.
- **Pydantic** – Data validation and serialization.
- **Argon2** – Secure password hashing algorithm.
- **Docker** – Application containerization.
- **Docker Compose** – Container orchestration.
- **pgAdmin 4** – Database management interface.
- **Pytest** – Automated testing framework.
- **Playwright** – End-to-end browser testing.
- **GitHub Actions** – Continuous integration and deployment.
- **Trivy** – Docker image vulnerability scanning.
- **Docker Hub** – Container image repository.

## Application Features

### Calculator Operations

The application supports the following calculation operations:

- Addition
- Subtraction
- Multiplication
- Division
- Division-by-zero validation

A calculation factory is used to select and execute the appropriate operation based on the requested calculation type.

### Calculation Model

The new SQLAlchemy `Calculation` model stores calculation information in PostgreSQL.

| Column | Data Type | Description |
|---|---|---|
| id | INTEGER | Unique calculation identifier |
| a | FLOAT | First operand |
| b | FLOAT | Second operand |
| type | VARCHAR(10) | Calculation operation |

The calculation type is restricted to the supported operations: `Add`, `Sub`, `Multiply`, and `Divide`.

The calculation result is computed when the data is returned through the Pydantic response schema. It is not stored as a separate database column.

### User Management API

The application also includes user registration and retrieval endpoints.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users/register` | Register a new user |
| GET | `/users/` | Retrieve all users |
| GET | `/users/{user_id}` | Retrieve a user by ID |

### Password Security

User passwords are securely hashed using Argon2 before being stored in PostgreSQL.

The application uses the `pwdlib` library to generate and verify password hashes.

Plain-text passwords and password hashes are not included in API responses.

### Data Validation

Pydantic schemas validate incoming information before it is processed.

For calculations, the `CalculationCreate` schema validates:

- The first and second operands.
- The requested calculation type.
- Division-by-zero errors.
- Non-finite numerical values.
- Unexpected additional fields.

The `CalculationRead` schema controls the information returned and includes the calculated result.

## Database Design

The PostgreSQL database is named `fastapi_db`.

### Users Table

| Column | Data Type | Description |
|---|---|---|
| id | INTEGER | Unique user identifier |
| username | VARCHAR(50) | Unique username |
| email | VARCHAR(100) | Unique email address |
| password_hash | VARCHAR(255) | Securely hashed password |
| created_at | TIMESTAMP | Account creation timestamp |

Both username and email have unique constraints to prevent duplicate registrations.

### Calculations Table

| Column | Data Type | Description |
|---|---|---|
| id | INTEGER | Unique calculation identifier |
| a | FLOAT | First operand |
| b | FLOAT | Second operand |
| type | VARCHAR(10) | Calculation operation |

The calculation model uses SQLAlchemy to define the database structure. A database constraint also helps prevent unsupported calculation types from being stored.

## Running the Project with Docker Compose

### Prerequisites

Install the following before running the project:

- Docker Desktop
- Docker Compose
- Git

### 1. Clone the repository

```bash
git clone https://github.com/zca3-ui/Module-11-FastAPI-PostgreSQL.git
cd Module-11-FastAPI-PostgreSQL
```

### 2. Build and start the containers

```bash
docker compose up --build -d
```

This command builds the FastAPI application image and starts the services defined in Docker Compose.

### 3. Verify the containers

```bash
docker compose ps
```

Confirm that the application, PostgreSQL, and pgAdmin containers are running.

### 4. Access the application

- FastAPI API documentation: http://localhost:8000/docs
- Health endpoint: http://localhost:8000/health
- pgAdmin: http://localhost:5050

## Connecting to PostgreSQL Through pgAdmin

Open pgAdmin at:

http://localhost:5050

Use the default login credentials configured in Docker Compose:

- Email: `admin@example.com`
- Password: `admin`

Register a PostgreSQL server using the following connection information:

| Setting | Value |
|---|---|
| Server Name | FastAPI PostgreSQL |
| Host | `postgres_db` |
| Port | 5432 |
| Maintenance Database | `fastapi_db` |
| Username | `postgres` |
| Password | `postgres` |

The hostname is `postgres_db` because pgAdmin and PostgreSQL communicate through the Docker Compose network.

## Running Automated Tests Locally

The project includes unit tests, integration tests, and end-to-end tests using Pytest.

### 1. Navigate to the project directory

```bash
cd Module-11-FastAPI-PostgreSQL
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start PostgreSQL

The integration and end-to-end tests require a running PostgreSQL database.

If using Docker Compose, start the database:

```bash
docker compose up -d postgres_db
```

The tests use the following default local database connection:

```text
postgresql+psycopg://postgres:postgres@localhost:5432/fastapi_db
```

### 5. Initialize the database

Run the following commands to create the users table and add password hashing support:

```bash
docker exec -i postgres_db psql -U postgres -d fastapi_db < sql/01_schema.sql
```

```bash
docker exec -i postgres_db psql -U postgres -d fastapi_db < sql/04_add_password_hash.sql
```

Create the SQLAlchemy tables, including the new calculation model:

```bash
python -c "from app.database.connection import Base, engine; from app.database.models import User, Calculation; Base.metadata.create_all(bind=engine)"
```

### 6. Install the Playwright browser

```bash
playwright install chromium
```

### 7. Run the tests

Run all tests:

```bash
python -m pytest -v
```

You can also run each test category separately.

**Unit tests**

```bash
python -m pytest tests/unit/ -v
```

**Integration tests**

```bash
python -m pytest tests/integration/ -v
```

**End-to-end tests**

```bash
python -m pytest tests/e2e/ -v
```

The unit tests check calculation operations, factory functionality, and input validation. Integration tests check database interactions and validation. End-to-end tests verify application functionality.

## Continuous Integration and Deployment (CI/CD)

GitHub Actions is used to automate the testing and Docker deployment process.

When changes are pushed to the `main` branch, the workflow:

1. Checks out the repository.
2. Sets up Python and installs dependencies.
3. Initializes the PostgreSQL database.
4. Runs unit, integration, and end-to-end tests.
5. Builds the Docker image.
6. Scans the image for vulnerabilities using Trivy.
7. Logs in to Docker Hub.
8. Pushes the Docker image to the repository.

The Docker deployment job runs after the test job succeeds.

## Docker Hub Repository

The Docker image for this project is published on Docker Hub:

**[FastAPI Calculation API – Docker Hub](https://hub.docker.com/repository/docker/zca3/fastapi-calculation-api/general)**

The workflow publishes the `latest` tag and a commit-specific image tag.

## GitHub Repository

**[Module 11 – FastAPI PostgreSQL](https://github.com/zca3-ui/Module-11-FastAPI-PostgreSQL)**