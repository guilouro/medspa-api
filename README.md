# Medspa API

A scalable API for managing medical spa services, appointments, and operations created with FastAPI.

## Project Overview

The Medspa API is a FastAPI-based backend service that provides a comprehensive solution for managing medical spa operations. It handles medspa profiles, service catalogs, and appointment scheduling with a focus on reliability and scalability.

## Tech Stack

- **Language**: Python 3.x
- **Framework**: FastAPI
- **ORM**: SQLModel (SQLAlchemy-based)
- **Database**: PostgreSQL
- **Testing**: Pytest
- **Code Quality**: Ruff
- **Containerization**: Docker
- **Deployment**: Fly.io
- **Documentation**: OpenAPI (Swagger UI)

## Architecture

The application follows a clean architecture pattern with the following components:

- **Routes**: Handle HTTP requests and response formatting
- **Models**: Define database schemas and relationships
- **Repositories**: Manage database operations and business logic
- **Database**: Handles database connections and migrations

## API Endpoints

The API provides the following main endpoints:

### Medspa Management
- `GET /medspas` - List all medspas
- `GET /medspas/{id}` - Get medspa details
- `POST /medspas` - Create new medspa
- `PUT /medspas/{id}` - Update medspa
- `DELETE /medspas/{id}` - Delete medspa

### Services Management
- `GET /services` - List all services
- `GET /services/{id}` - Get service details
- `POST /services` - Create new service
- `PUT /services/{id}` - Update service
- `DELETE /services/{id}` - Delete service

### Appointments Management
- `GET /appointments` - List all appointments
- `GET /appointments/{id}` - Get appointment details
- `POST /appointments` - Create new appointment
- `PUT /appointments/{id}` - Update appointment
- `DELETE /appointments/{id}` - Delete appointment

For detailed API documentation, visit `/docs` when running the application.

## API Call Examples

For detailed API call examples, visit the list of examples here: [API Call Examples](api-call-examples.md).

## Database

The database schema, in its first and simple version, consists of the following main entities and follows this DBML structure:

<details>
<summary>Simple DBML Schema</summary>

```dbml
// Medspa 
Table medspa {
  id integer [primary key]
  name varchar
  address varchar
  phone_number varchar
  email_address varchar
  created_at datetime
  updated_at datetime
}

// Service
Table services {
  id integer [primary key]
  medspa_id integer [ref: > medspa.id]
  name varchar
  description text
  price decimal(10,2)
  duration integer
  created_at datetime
  updated_at datetime
}

enum appointment_status {
  scheduled
  completed
  canceled
}

// Appointment
Table appointments {
  id integer [primary key]
  medspa_id integer [ref: > medspa.id]
  start_time timestamp
  total_duration integer
  total_price decimal(10,2)
  status appointment_status
  created_at datetime
  updated_at datetime
}

Table appointments_services {
  appointment_id integer [ref: > appointments.id]
  service_id integer [ref: > services.id]

  indexes {
    (appointment_id, service_id) [pk]
  }
}
```
</details>

You can visualize this database schema using the following diagram:

![Database Schema](.github/images/dbml.png)


- **Medspa**: Stores medspa information
- **Services**: Manages available services
- **Appointments**: Handles appointment scheduling
- **AppointmentsServices**: Junction table for appointment-service relationships

Key features:
- Automatic timestamp management (created_at, updated_at)
- Relationship cascading
- Decimal precision for monetary values
- Enum-based status management

--- 

Here a more robust schema with more fields and relationships:

<details>
<summary>Robust DBML Schema</summary>

```dbml
// Medspa 
Table medspa {
  id integer [primary key]
  name varchar
  address varchar
  phone_number varchar
  email_address varchar
  created_at datetime
  updated_at datetime
}

// Service
Table services {
  id integer [primary key]
  medspa_id integer [ref: > medspa.id]
  service_type_id int [ref: > service_types.id]
  supplier_id int [ref: - suppliers.id, null]
  name varchar
  description text
  price decimal(10,2)
  currency varchar
  duration integer
  supplier varchar [null] 
  created_at datetime
  updated_at datetime
}

// Service Categories
Table service_categories {
  id integer [primary key]
  name varchar
  created_at datetime
  updated_at datetime
}

//Service Types
Table service_types {
  id integer [primary key]
  service_category_id integer [ref: > service_categories.id]
  name varchar
  created_at datetime
  updated_at datetime
}

Table suppliers {
  id integer [primary key]
  name varchar
}

enum appointment_status {
  scheduled
  completed
  canceled
}

// Appointment
Table appointments {
  id integer [primary key]
  medspa_id integer [ref: > medspa.id]
  start_time timestamp
  total_duration integer
  total_price decimal(10,2)
  status appointment_status
  created_at datetime
  updated_at datetime
}

Table appointments_services {
  appointment_id integer [ref: > appointments.id]
  service_id integer [ref: > services.id]

  indexes {
    (appointment_id, service_id) [pk]
  }
}

```
</details>

You can visualize this database schema using the following diagram:

![Database Schema](.github/images/dbml2.png)


- **Medspa**: Stores medspa information
- **Services**: Manages available services
- **Appointments**: Handles appointment scheduling
- **AppointmentsServices**: Junction table for appointment-service relationships
- **ServiceCategories**: Manages service categories
- **ServiceType**: Manages service types



## Testing

The project uses Pytest for testing with the following structure:

```
tests/
├── conftest.py      # Test fixtures and configuration
├── test_medspa.py   # Medspa-related tests
├── test_services.py # Service-related tests
└── test_appointments.py # Appointment-related tests
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_medspa.py
```

## Deployment

The application is deployed on Fly.io with the following features:

### CI/CD Pipeline

The project uses GitHub Actions for continuous integration:
- Automated testing
- Code quality checks
- Docker image building
- Deployment to Fly.io

![CI/CD Pipeline](.github/images/action.png)


## Running Locally

1. Create and activate a virtual environment:
```bash
python -m venv venv_medspa
source venv_medspa/bin/activate  # On Windows: venv_medspa\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env-sample .env
# Edit .env with your configuration
```

4. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Running Tests

1. Ensure you're in the project directory and your virtual environment is activated

2. Run the test suite:
```bash
pytest
```

3. For coverage report:
```bash
pytest --cov=.
```

4. For specific test files:
```bash
pytest tests/test_medspa.py
pytest tests/test_services.py
pytest tests/test_appointments.py
```

## Formatting and Linting

The project uses Ruff for formatting and linting.

```bash
ruff check .
```

To fix linting errors automatically:
```bash
ruff check --fix .
```

To format the code: 
```bash
ruff format .
```

## Using Docker compose to run the database locally

Before running docker compose, set the DATABASE_URL environment variable in the .env file:

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/medspa_db
```

Then, run the following command:
```bash
docker compose up -d
```

## Seed

To seed the database with data, run the following command:
```bash
python seed.py
```


