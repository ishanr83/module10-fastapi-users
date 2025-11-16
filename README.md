# FastAPI Secure User Management

## Student Information
- **Name:** Ishan Rehan
- **Email:** ir83@njit.edu
- **Course:** IS 601
- **Assignment:** Module 10 - Secure User Model, Pydantic Validation, Testing & Docker Deployment

## Project Overview
This FastAPI application implements secure user management with:
- SQLAlchemy ORM for database operations
- Pydantic schemas for data validation
- bcrypt password hashing
- Comprehensive unit and integration tests
- CI/CD pipeline with GitHub Actions
- Docker containerization and Docker Hub deployment

## Features
- ✅ Secure password hashing with bcrypt
- ✅ Email validation using Pydantic
- ✅ Unique constraints on username and email
- ✅ RESTful API endpoints for user management
- ✅ Automated testing with pytest
- ✅ CI/CD pipeline with GitHub Actions
- ✅ Docker containerization
- ✅ PostgreSQL database integration

## Technologies Used
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation and serialization
- **PostgreSQL** - Relational database
- **bcrypt** - Password hashing algorithm
- **pytest** - Testing framework
- **Docker** - Containerization
- **GitHub Actions** - CI/CD automation

## Prerequisites
- Python 3.11+
- Docker Desktop
- PostgreSQL (or use Docker Compose)
- Git

## Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ishanr83/module10-fastapi-users.git
cd module10-fastapi-users
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Mac/Linux
# or
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Database
#### Option A: Using Docker Compose (Recommended)
```bash
docker-compose up -d db
```

#### Option B: Local PostgreSQL
```bash
# Create database
createdb fastapi_db

# Set environment variable
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/fastapi_db"
```

### 5. Run the Application
```bash
uvicorn app.main:app --reload
```

Access the application:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Running Tests Locally

### Run All Tests
```bash
pytest -v
```

### Run Specific Test Files
```bash
# Unit tests for password hashing
pytest tests/test_auth.py -v

# Unit tests for Pydantic schemas
pytest tests/test_schemas.py -v

# Integration tests for API endpoints
pytest tests/test_api.py -v
```

### Run Tests with Coverage
```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

### Test Database Setup
Tests use a separate test database. Set the environment variable:
```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/test_db"
```

Or let pytest use the default test database configuration.

## Docker Deployment

### Build Docker Image
```bash
docker build -t fastapi-users:latest .
```

### Run with Docker Compose
```bash
docker-compose up --build
```

This starts:
- PostgreSQL database on port 5432
- FastAPI application on port 8000

### Stop Services
```bash
docker-compose down
```

### Remove Volumes (Delete Data)
```bash
docker-compose down -v
```

## Docker Hub

The Docker image is automatically built and pushed to Docker Hub via GitHub Actions.

**Docker Hub Repository:** https://hub.docker.com/r/ishanr83/fastapi-users

### Pull and Run from Docker Hub
```bash
# Pull the image
docker pull ishanr83/fastapi-users:latest

# Run with PostgreSQL
docker run -d --name postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=fastapi_db \
  -p 5432:5432 \
  postgres:15-alpine

# Run the application
docker run -d --name fastapi-app \
  -e DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/fastapi_db \
  -p 8000:8000 \
  ishanr83/fastapi-users:latest
```

## API Endpoints

### User Management

#### Create User
```http
POST /users
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepass123"
}
```

#### Get All Users
```http
GET /users?skip=0&limit=100
```

#### Get User by ID
```http
GET /users/{user_id}
```

#### Delete User
```http
DELETE /users/{user_id}
```

### Health Check
```http
GET /health
```

## CI/CD Pipeline

The project uses GitHub Actions for automated testing and deployment.

### Workflow Steps:
1. **Test Job:**
   - Sets up Python environment
   - Installs dependencies
   - Runs unit tests (auth, schemas)
   - Runs integration tests with PostgreSQL container
   
2. **Build and Push Job** (only on main branch):
   - Builds Docker image
   - Pushes to Docker Hub with tags:
     - `latest`
     - Git commit SHA

### GitHub Secrets Required:
- `DOCKER_USERNAME` - Your Docker Hub username
- `DOCKER_PASSWORD` - Your Docker Hub password or access token

## Project Structure
cat > README.md << 'EOF'
# FastAPI Secure User Management

## Student Information
- **Name:** Ishan Rehan
- **Email:** ir83@njit.edu
- **Course:** IS 601
- **Assignment:** Module 10 - Secure User Model, Pydantic Validation, Testing & Docker Deployment

## Project Overview
This FastAPI application implements secure user management with:
- SQLAlchemy ORM for database operations
- Pydantic schemas for data validation
- bcrypt password hashing
- Comprehensive unit and integration tests
- CI/CD pipeline with GitHub Actions
- Docker containerization and Docker Hub deployment

## Features
- ✅ Secure password hashing with bcrypt
- ✅ Email validation using Pydantic
- ✅ Unique constraints on username and email
- ✅ RESTful API endpoints for user management
- ✅ Automated testing with pytest
- ✅ CI/CD pipeline with GitHub Actions
- ✅ Docker containerization
- ✅ PostgreSQL database integration

## Technologies Used
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation and serialization
- **PostgreSQL** - Relational database
- **bcrypt** - Password hashing algorithm
- **pytest** - Testing framework
- **Docker** - Containerization
- **GitHub Actions** - CI/CD automation

## Prerequisites
- Python 3.11+
- Docker Desktop
- PostgreSQL (or use Docker Compose)
- Git

## Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ishanr83/module10-fastapi-users.git
cd module10-fastapi-users
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Mac/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Database
```bash
docker-compose up -d db
```

### 5. Run the Application
```bash
uvicorn app.main:app --reload
```

Access the application:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Running Tests Locally

### Run All Tests
```bash
pytest -v
```

### Run Specific Test Files
```bash
pytest tests/test_auth.py -v
pytest tests/test_schemas.py -v
pytest tests/test_api.py -v
```

### Run Tests with Coverage
```bash
pytest --cov=app --cov-report=html
```

### Test Database Setup
```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/test_db"
pytest -v
```

## Docker Deployment

### Build Docker Image
```bash
docker build -t fastapi-users:latest .
```

### Run with Docker Compose
```bash
docker-compose up --build
```

### Stop Services
```bash
docker-compose down
```

## Docker Hub

**Docker Hub Repository:** https://hub.docker.com/r/ishanr83/fastapi-users

### Pull and Run from Docker Hub
```bash
docker pull ishanr83/fastapi-users:latest

docker run -d --name postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=fastapi_db \
  -p 5432:5432 \
  postgres:15-alpine

docker run -d --name fastapi-app \
  -e DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/fastapi_db \
  -p 8000:8000 \
  ishanr83/fastapi-users:latest
```

## API Endpoints

### Create User
```http
POST /users
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepass123"
}
```

### Get All Users
```http
GET /users?skip=0&limit=100
```

### Get User by ID
```http
GET /users/{user_id}
```

### Delete User
```http
DELETE /users/{user_id}
```

### Health Check
```http
GET /health
```

## CI/CD Pipeline

GitHub Actions automatically:
1. Runs all tests on push/pull request
2. Builds Docker image on main branch
3. Pushes to Docker Hub with tags (latest and commit SHA)

### GitHub Secrets Required
- `DOCKER_USERNAME` - Your Docker Hub username
- `DOCKER_PASSWORD` - Your Docker Hub password or access token

## Project Structure
```
module10-fastapi-users/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── auth.py          # Password hashing utilities
│   └── database.py      # Database configuration
├── tests/
│   ├── __init__.py
│   ├── test_auth.py     # Unit tests for auth
│   ├── test_schemas.py  # Unit tests for schemas
│   └── test_api.py      # Integration tests for API
├── .github/
│   └── workflows/
│       └── ci-cd.yml    # GitHub Actions workflow
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

## Security Features

### Password Hashing
- Uses bcrypt algorithm
- Passwords never stored in plain text
- Each password gets unique salt
- Secure password verification

### Data Validation
- Pydantic EmailStr validates email format
- Username: 3-50 characters
- Password: Minimum 8 characters
- Unique constraints enforced

### Database Security
- Parameterized queries prevent SQL injection
- Foreign key constraints
- Non-root Docker user

## Testing Strategy

### Unit Tests
- Password hashing functions
- Password verification
- Pydantic schema validation
- Edge cases and error handling

### Integration Tests
- API endpoint functionality
- Database operations
- Duplicate username/email prevention
- User CRUD operations

## Troubleshooting

### Database Connection Issues
```bash
docker-compose down -v
docker-compose up -d db
sleep 5
pytest -v
```

### Port Conflicts
```bash
lsof -i :5432
lsof -i :8000
```

### Reset Database
```bash
docker-compose down -v
docker-compose up -d
```

## Learning Outcomes Achieved

✅ **CLO3:** Created Python application with automated testing using pytest  
✅ **CLO4:** Set up GitHub Actions for CI/CD with automated tests and Docker builds  
✅ **CLO9:** Applied containerization using Docker and Docker Compose  
✅ **CLO11:** Integrated Python with PostgreSQL database  
✅ **CLO12:** Used Pydantic for JSON serialization and validation  
✅ **CLO13:** Implemented secure authentication with bcrypt hashing  

## Author
Ishan Rehan (ir83@njit.edu)

## Date
November 15, 2024

## License
Educational project for IS 601 coursework
