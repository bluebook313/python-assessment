# Project Name

## Overview

This project is a FastAPI-based backend application designed with a layered architecture.

The application separates API endpoints, task execution, business logic, database models, and shared utilities into independent layers.

The main goal of this architecture is to keep the API layer simple and move business logic and database operations into appropriate layers.

---

## Features

* Product CRUD
* Customer management
* Order management
* Order / OrderItem relationship
* API versioning (`v1`, `v2`, ...)
* Task layer for executing application operations
* Service layer for business logic
* SQLAlchemy ORM
* Database session management
* Transaction and rollback handling
* Centralized exception handling
* Standardized API responses
* Swagger / OpenAPI documentation
* Docker support
* Test structure

---

# Architecture

The application follows a layered architecture:

```text
Client
  │
  ▼
API Layer
  │
  ▼
Task Layer
  │
  ▼
Service Layer
  │
  ▼
SQLAlchemy / Database
  │
  ▼
Database
```

Each layer has a specific responsibility.

## API Layer

The API layer is responsible for:

* Receiving HTTP requests
* Validating basic input
* Calling the appropriate Task
* Returning standardized responses
* Handling API versioning

The API layer should contain minimal business logic.

For example:

```python
@router.get("/customer/{customer_id}")
async def get_user_info(customer_id: int):
    if customer_id <= 0:
        return CustomResponse.response(
            status=http_status.HTTP_400_BAD_REQUEST,
            details="input must be bigger than 0",
            result={},
        )

    return await handle_task(
        task_class=GetCustomerInfoTasks,
        customer_id=customer_id,
    )
```

The endpoint does not directly call the Service layer. Instead, it delegates the operation to a Task.

---

# API Versioning

API endpoints are organized by version.

```text
app/
└── api/
    ├── v1/
    │   ├── customer/
    │   ├── product/
    │   └── order/
    │
    ├── v2/
    │   ├── customer/
    │   ├── product/
    │   └── order/
    │
    └── ...
```

This structure allows new versions of the API to be introduced without breaking existing clients.

For example:

```text
/api/v1/customer/{customer_id}
/api/v2/customer/{customer_id}
```

A new API version can change request/response formats or endpoint behavior while keeping the previous version available for existing clients.

---

# Task Layer

The Task layer acts as an intermediate layer between the API and Service layers.

Its responsibilities include:

* Executing application operations
* Receiving parameters from the API layer
* Creating or managing the database session
* Calling the appropriate Service
* Returning the Service result

Example:

```python
class GetCustomerInfoTasks:

    @staticmethod
    async def run(*args, **kwargs):
        with get_db() as db:
            return await CustomerService(
                db=db
            ).get_customer_info(**kwargs)
```

The API does not need to know how the database session or Service is managed.

Instead:

```text
API
 ↓
Task
 ↓
Service
```

This keeps the API endpoints small and easier to maintain.

---

# Service Layer

The Service layer contains the application's business logic.

Responsibilities include:

* Business rules
* Database operations
* Validation related to business rules
* Creating and updating entities
* Handling business-specific exceptions

Example:

```python
class ProductService:

    def __init__(self, db: Session):
        self.db = db

    async def add_item(
        self,
        name: str,
        price: int,
        count: int,
    ):
        ...
```

The Service receives a database session and performs the required business operation.

The Service layer should not depend on HTTP-specific concepts such as `HTTPException`.

---

# Database Layer

The database layer is responsible for:

* Creating SQLAlchemy sessions
* Managing database connections
* Providing the session to the application
* Closing sessions after operations are completed

The Service layer uses the SQLAlchemy session to perform database operations.

---

# Database Session Lifecycle

Database sessions must have a clear lifecycle.

The general flow is:

```text
Create Session
     │
     ▼
Execute Operation
     │
     ├── Success ──► Commit
     │
     └── Error ────► Rollback
     │
     ▼
Close Session
```

The session should not remain open after the operation has finished.

---

# Transaction Management

Database operations should be executed inside a transaction.

On successful execution:

```python
db.commit()
```

If an error occurs:

```python
db.rollback()
```

This prevents partially completed database operations from leaving the database in an inconsistent state.

---

# Error Handling

The application separates business exceptions from unexpected application errors.

Business logic errors use `ServiceException`.

Example:

```python
except ServiceException as e:
    status = http_status.HTTP_400_BAD_REQUEST
    details = str(e)
```

Unexpected errors are handled separately:

```python
except Exception as e:
    status = http_status.HTTP_500_INTERNAL_SERVER_ERROR
    details = str(e)
```

This allows the application to distinguish between:

```text
Business Error
     │
     └── 400 Bad Request

Unexpected Error
     │
     └── 500 Internal Server Error
```

---

# Standardized API Response

API responses are returned through `CustomResponse`.

Example:

```python
return CustomResponse.response(
    status=http_status.HTTP_200_OK,
    details="Task successfully submitted",
    result=result,
)
```

This provides a consistent response structure across different endpoints.

---

# Request Flow

A typical request follows this flow:

```text
HTTP Request
     │
     ▼
API Endpoint
     │
     ▼
handle_task()
     │
     ▼
Task.run()
     │
     ▼
Service
     │
     ▼
SQLAlchemy
     │
     ▼
Database
     │
     ▼
Service Result
     │
     ▼
CustomResponse
     │
     ▼
HTTP Response
```

For example:

```text
GET /customer/10
       │
       ▼
get_user_info()
       │
       ▼
GetCustomerInfoTasks
       │
       ▼
CustomerService
       │
       ▼
Database
```

---

# Orders

The relationship between `Order` and `OrderItem` is:

```text
Order
  │
  ├── OrderItem
  ├── OrderItem
  └── OrderItem
```

In database terms:

```text
Order 1 ──────── * OrderItem
```

One order can contain multiple order items.

`OrderItem` represents the products included in an order and stores information related to that specific order item.

---

# Project Structure

```text
project/
│
├── app/
│   │
│   ├── api/
│   │   ├── v1/
│   │   │   ├── customer/
│   │   │   ├── product/
│   │   │   └── order/
│   │   │
│   │   ├── v2/
│   │   │   └── ...
│   │   │
│   │   └── ...
│   │
│   ├── services/
│   │   ├── tasks/
│   │   │   ├── customer/
│   │   │   ├── product/
│   │   │   └── order/
│   │   │
│   │   └── ...
│   │
│   ├── models/
│   │
│   ├── schemas/
│   │
│   ├── utils/
│   │
│   ├── database/
│   │
│   └── main.py
│
├── docs/
│
├── test/
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── .env
├── .env_release
├── requirements.txt
└── README.md
```

---

# Directory Responsibilities

### `app/api/`

Contains HTTP API endpoints.

API versions are separated into directories such as:

```text
api/
├── v1/
├── v2/
└── ...
```

### `app/services/`

Contains application business logic and task execution.

```text
services/
└── tasks/
    ├── customer/
    ├── product/
    └── order/
```

### `app/models/`

Contains SQLAlchemy ORM models representing database entities.

Examples:

```text
Customer
Product
Order
OrderItem
```

### `app/schemas/`

Contains request and response schemas used for data validation and serialization.

### `app/utils/`

Contains shared application utilities such as:

* Custom exceptions
* API response helpers
* Common utilities


### `app/main.py`

Application entry point.

It is responsible for creating the FastAPI application and registering routers.

### `docs/`

Contains project documentation and technical documentation.

### `test/`

Contains automated tests for the application.

---

# Installation

## Requirements

* Python 3.x
* FastAPI
* SQLAlchemy
* Uvicorn
* Database

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Configuration

Application configuration is managed through environment files.

```text
.env
.env_release
```

Typical configuration may include:

```text
DATABASE_URL
```

Environment files should not contain sensitive information in source control.

---

# Run the Application

From the project root:

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://localhost:8000
```

---

# API Documentation

FastAPI automatically provides OpenAPI documentation.

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

# Docker

The project also contains Docker configuration.

Use Docker compose :

```bash
docker compose up --build -d  
```

See container log:

```bash
docker logs -f shopping-project
```


---

# Design Assumptions

The project follows these design principles:

* API endpoints should remain simple.
* Business logic belongs in the Service layer.
* API endpoints should not directly implement database operations.
* Tasks provide a separation between API execution and Services.
* Database sessions should have a clearly defined lifecycle.
* Transactions should support commit and rollback.
* Business exceptions should be separated from unexpected exceptions.
* API responses should follow a consistent structure.
* API versions should be isolated to prevent breaking existing clients.
* SQLAlchemy ORM is used for database interaction.
* Database models and API schemas have separate responsibilities.

---

# Development Guidelines

When adding a new feature, follow the existing architecture:

```text
1. Define Model
      ↓
2. Define Schema
      ↓
3. Implement Service
      ↓
4. Implement Task
      ↓
5. Add API Endpoint
      ↓
6. Add Tests
```

For example, adding a new Product operation should generally follow:

```text
Product API
    ↓
Product Task
    ↓
Product Service
    ↓
SQLAlchemy
    ↓
Database
```

This structure keeps responsibilities separated and makes the application easier to maintain and extend.
