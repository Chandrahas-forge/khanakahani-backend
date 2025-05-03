# Khana Kahani API

Khana Kahani API is a Recipe Management System built with FastAPI, SQLAlchemy, and PostgreSQL. It supports user authentication (with JWT), recipe CRUD operations, favorites, and recipe notes. The project is containerized using Docker and uses Alembic for database migrations.

## Features

- **User Authentication:**  
  Register, login, and logout endpoints with JWT token support.

- **Recipe Management:**  
  Create, update, list (with pagination & filtering), retrieve, and delete recipes.  
  Each recipe includes title, cuisine, a list of ingredients, tags, and steps.

- **Recipe Notes & Favorites:**  
  Add notes to recipes and mark recipes as favorites.

- **OpenAPI Documentation:**  
  Automatic API docs available via Swagger UI and ReDoc.

- **Database Migrations:**  
  Managed using Alembic.

- **Dockerized:**  
  The backend and database run in Docker containers with a docker-compose configuration.

## Project Structure

```
KhanaKahaniCore/
├── alembic/
│   ├── env.py
│   ├── versions/
│   ├── alembic.ini
│   └── script.py.mako
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   ├── recipes.py
│   │   └── users.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── crud/
│   │   ├── crud_recipe.py
│   │   └── crud_user.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   ├── base_class.py
│   │   ├── recipe.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── recipe.py
│   │   └── user.py
│   ├── main.py
│   └── entrypoint.sh
├── tests/
│   ├── test_endpoints.py
│   └── test_main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- PostgreSQL
- Docker & Docker Compose (for containerized deployment)
- [pipenv or virtualenv](https://docs.python.org/3/tutorial/venv.html) is recommended for development

### Environment Variables

Create a `.env` file in the project root. An example is already provided:

```
POSTGRES_USER=khanakahaniuser
POSTGRES_PASSWORD=GreenChef2504
POSTGRES_DB=khanakahanidb
SQLALCHEMY_DATABASE_URL=postgresql://khanakahaniuser:GreenChef2504@localhost:5432/khanakahanidb

SECRET_KEY=supersecret_jwt_signing_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **Note:** When running via Docker, the `host` for the database in the connection URL might need to be updated as per your container configuration.

## Running the Application

### Locally

1. **Create & Activate Virtual Environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**  
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Run Alembic Migrations**  
   ```bash
   alembic upgrade head
   ```

4. **Start the FastAPI Application**  
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access Documentation:**  
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)  
   - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Using Docker

1. **Build and Start Containers**  
   From the project root, run:  
   ```bash
   docker-compose up --build
   ```
   This will build the Docker image, start the PostgreSQL container, run Alembic migrations (via the entrypoint script), and run the FastAPI server.

2. **Access API & Documentation**  
   Visit [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI, or use your frontend application to interact with the API.

## Running Tests

To run the automated tests using pytest, execute:

```bash
pytest
```

Tests are located in the `/tests` directory and include endpoints for authentication, recipes, and more.

## API Documentation

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI JSON:** [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

## Database Migrations

Database schema migrations are handled with Alembic. Use the following commands:

- **Create a New Revision:**  
  ```bash
  alembic revision --autogenerate -m "Description of changes"
  ```

- **Apply Migrations:**  
  ```bash
  alembic upgrade head
  ```

The alembic configuration is defined in `alembic.ini` and the migration scripts are located in the `alembic/versions` directory.

## Contributing

Contributions and suggestions are welcome! Please create an issue or submit a pull request.

## License

This project is licensed under the MIT License.
