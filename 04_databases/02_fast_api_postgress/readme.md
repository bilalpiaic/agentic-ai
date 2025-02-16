# FastAPI To-Do App with Alembic and PostgreSQL

## Installation
To set up the project with Alembic and PostgreSQL, install the required dependencies:
```sh
uv add alembic
uv add psycopg2-binary
```

## New Project Setup
Follow these steps to initialize Alembic and configure it for database migrations:

1. **Initialize Alembic**
   ```sh
   uv run alembic init alembic
   ```
2. **Set the Database URL**
   - Locate the `alembic.ini` file.
   - Modify the `sqlalchemy.url` entry to point to your PostgreSQL database, e.g.:
     ```ini
     sqlalchemy.url = postgresql+psycopg2://user:password@localhost/dbname
     ```

3. **Create SQLAlchemy Model**
   - Define a SQLAlchemy model for your table, for example:
     ```python
     from sqlalchemy import Column, Integer, String
     from sqlalchemy.ext.declarative import declarative_base

     Base = declarative_base()

     class Todo(Base):
         __tablename__ = 'todos'
         id = Column(Integer, primary_key=True, index=True)
         title = Column(String, nullable=False)
         description = Column(String, nullable=True)
     ```

4. **Set Target Metadata in Alembic**
   - Open `alembic/env.py` and update the target metadata:
     ```python
     from models import Base  # Import the model base
     target_metadata = Base.metadata
     ```

## Running Migrations
Whenever you make changes to your models, run the following commands:

1. **Generate Migration Script**
   ```sh
   uv run alembic revision --autogenerate -m "create todos table"
   ```

2. **Apply Migrations**
   ```sh
   uv run alembic upgrade head
   ```

This will create and apply the necessary database schema changes based on your models.

