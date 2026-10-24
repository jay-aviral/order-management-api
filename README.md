# Order Management API

![CI](https://github.com/jay-aviral/order-management-api/actions/workflows/ci.yml/badge.svg)

A REST API for managing users, products and orders, built with FastAPI and PostgreSQL.

## Features

- User registration and login with JWT authentication
- Role-based access control (admin and customer)
- Product management (create, read, update, delete) with search and pagination
- Order placement with stock checking and automatic stock reduction
- Customers see only their own orders; admins can update order status
- Database migrations with Alembic
- Automated tests with pytest and CI with GitHub Actions
- Docker setup for one-command startup

## Tech stack

Python, FastAPI, SQLAlchemy, PostgreSQL, Alembic, Pydantic, JWT, Docker, pytest, GitHub Actions

## Run with Docker

```bash
git clone https://github.com/jay-aviral/order-management-api.git
cd order-management-api
docker compose up --build
```

Open http://localhost:8000/docs to see the interactive API documentation.

## Run locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker compose up -d db
alembic upgrade head
uvicorn app.main:app --reload
```

## Run the tests

```bash
pytest --cov=app
```

## API endpoints

| Method | Path | Access |
|---|---|---|
| POST | /auth/register | Public |
| POST | /auth/login | Public |
| GET | /products | Public |
| GET | /products/{id} | Public |
| POST | /products | Admin |
| PUT | /products/{id} | Admin |
| DELETE | /products/{id} | Admin |
| POST | /orders | Logged-in user |
| GET | /orders | Logged-in user (own orders) |
| GET | /orders/{id} | Owner or admin |
| PATCH | /orders/{id}/status | Admin |

## Project structure

```
app/
  core/       settings and security (JWT, password hashing)
  db/         database session
  models/     SQLAlchemy models
  schemas/    Pydantic schemas
  routers/    API endpoints
alembic/      database migrations
tests/        pytest tests
```

## Future improvements

- Redis caching for the product list
- Background jobs with Celery (order emails)
- Rate limiting
- Cloud deployment
