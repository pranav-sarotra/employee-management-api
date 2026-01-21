# 🏢 Employee Management API

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)

A **production-grade RESTful API** for managing employee information, built with **FastAPI** and **MongoDB**.

🔗 <b>Deployed API:</b>

<a href="https://employee-management-api-psbq.onrender.com/docs" style="text-decoration:none;">
  <img
    src="https://img.shields.io/badge/Live%20Demo-blue?style=for-the-badge"
    alt="Live Demo"
    height="256"
    style="vertical-align:middle;"
  />
</a>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| ✅ **CRUD Operations** | Create, Read, Update, Delete employees |
| ✅ **Pagination** | Efficiently handle large datasets with page & limit |
| ✅ **Filtering** | Filter employees by department |
| ✅ **Input Validation** | Strict validation using Pydantic models |
| ✅ **Unique ID Enforcement** | Database-level duplicate prevention |
| ✅ **Structured Logging** | Professional logging with timestamps |
| ✅ **Dependency Injection** | Testable and maintainable code architecture |
| ✅ **Environment Config** | Secure settings via environment variables |
| ✅ **Interactive Docs** | Auto-generated Swagger UI & ReDoc |
| ✅ **CORS Enabled** | Ready for frontend integration |

---

## 🛠 Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| ![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white) | 3.10+ | Programming Language |
| ![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-teal?logo=fastapi&logoColor=white) | 0.104.1 | Web Framework |
| ![MongoDB](https://img.shields.io/badge/MongoDB-7.0-green?logo=mongodb&logoColor=white) | 7.0 | NoSQL Database |
| ![Motor](https://img.shields.io/badge/Motor-3.3.2-green) | 3.3.2 | Async MongoDB Driver |
| ![Pydantic](https://img.shields.io/badge/Pydantic-2.5.2-red) | 2.5.2 | Data Validation |
| ![Uvicorn](https://img.shields.io/badge/Uvicorn-0.24.0-purple) | 0.24.0 | ASGI Server |

---

## 📂 Project Structure

```text
employee_management_api/
│
├── 📂 app/
│   ├── 📄 __init__.py # Package initialization
│   ├── 📄 main.py # FastAPI application entry point
│   ├── 📄 config.py # Configuration management
│   ├── 📄 database.py # MongoDB connection & dependency injection
│   │
│   ├── 📂 models/
│   │   ├── 📄 __init__.py # Models package
│   │   ├── 📄 employee.py # Pydantic models & Department Enum
│   │
│   ├── 📂 routers/
│   │   ├── 📄 __init__.py # Routers package
│   │   ├── 📄 employees.py # CRUD API endpoints
│   │
│   ├── 📂 utils/
│       ├── 📄 __init__.py # Utils package
│       ├── 📄 logger.py # Logging configuration
│
├── 📄 .env.example # Environment variables template
├── 📄 .gitignore # Git ignore rules
├── 📄 LICENSE # MIT License
├── 📄 README.md # Project documentation
├── 📄 requirements.txt # Python dependencies
└── 📄 run.py # Application runner script
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher  
- MongoDB (local or MongoDB Atlas)  
- Git  

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/employee-management-api.git
cd employee-management-api

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables
cp .env.example .env
# Edit .env with your MongoDB connection string

# 6. Run the application
python run.py
```

### Access the API

| URL | Description |
|-----|-------------|
| [http://localhost:8000](http://localhost:8000) | API Root |
| [http://localhost:8000/docs](http://localhost:8000/docs) | Swagger UI Documentation |
| [http://localhost:8000/redoc](http://localhost:8000/redoc) | ReDoc Documentation |
| [http://localhost:8000/health](http://localhost:8000/health) | Health Check |

---

## 🧾 API Endpoints

### Employee Operations

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/employees` | Create a new employee | No |
| GET | `/employees` | Get all employees (paginated) | No |
| GET | `/employees/{employee_id}` | Get employee by ID | No |
| PATCH | `/employees/{employee_id}` | Update employee (partial) | No |
| DELETE | `/employees/{employee_id}` | Delete employee | No |

### Utility Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/employees/meta/departments` | List valid departments |

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number (min: 1) |
| `limit` | integer | 10 | Items per page (min: 1, max: 100) |
| `department` | string | `null` | Filter by department |

---

## 🗂 Valid Departments

The API accepts only these department values:

| Department | Enum Value |
|-----------|------------|
| Engineering | `Engineering` |
| Marketing | `Marketing` |
| Finance | `Finance` |
| Human Resources | `Human Resources` |
| Sales | `Sales` |
| Operations | `Operations` |
| Information Technology | `Information Technology` |
| Legal | `Legal` |
| Customer Service | `Customer Service` |
| Research and Development | `Research and Development` |

---

## 💻 API Examples

### Create Employee

**Request:**

```bash
curl -X POST "http://localhost:8000/employees" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "EMP001",
    "name": "John Doe",
    "age": 30,
    "department": "Engineering"
  }'
```

**Response (201 Created):**

```json
{
  "message": "Employee created successfully",
  "data": {
    "employee": {
      "employee_id": "EMP001",
      "name": "John Doe",
      "age": 30,
      "department": "Engineering"
    }
  }
}
```

---

### Get All Employees (Paginated)

**Request:**

```bash
curl -X GET "http://localhost:8000/employees?page=1&limit=10"
```

**Response (200 OK):**

```json
{
  "total_count": 25,
  "page": 1,
  "limit": 10,
  "employees": [
    {
      "employee_id": "EMP001",
      "name": "John Doe",
      "age": 30,
      "department": "Engineering"
    },
    {
      "employee_id": "EMP002",
      "name": "Jane Smith",
      "age": 28,
      "department": "Marketing"
    }
  ]
}
```

---

### Filter by Department

**Request:**

```bash
curl -X GET "http://localhost:8000/employees?department=Engineering"
```

---

### Get Single Employee

**Request:**

```bash
curl -X GET "http://localhost:8000/employees/EMP001"
```

**Response (200 OK):**

```json
{
  "employee_id": "EMP001",
  "name": "John Doe",
  "age": 30,
  "department": "Engineering"
}
```

---

### Update Employee (Partial)

**Request:**

```bash
curl -X PATCH "http://localhost:8000/employees/EMP001" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 31,
    "department": "Information Technology"
  }'
```

**Response (200 OK):**

```json
{
  "message": "Employee updated successfully",
  "data": {
    "employee": {
      "employee_id": "EMP001",
      "name": "John Doe",
      "age": 31,
      "department": "Information Technology"
    }
  }
}
```

---

### Delete Employee

**Request:**

```bash
curl -X DELETE "http://localhost:8000/employees/EMP001"
```

**Response (200 OK):**

```json
{
  "message": "Employee deleted successfully",
  "data": {
    "deleted_employee_id": "EMP001"
  }
}
```

---

### Error Responses

#### 400 Bad Request (Duplicate ID):

```json
{
  "detail": "Employee with ID 'EMP001' already exists"
}
```

#### 404 Not Found:

```json
{
  "detail": "Employee with ID 'EMP999' not found"
}
```

#### 422 Validation Error:

```json
{
  "detail": [
    {
      "type": "greater_than_equal",
      "loc": [
        "body",
        "age"
      ],
      "msg": "Input should be greater than or equal to 18",
      "input": 15
    }
  ]
}
```

---

## 🌐 Deployment

This API is deployed using:

- **Backend Hosting:** [Render](https://render.com) (Free Tier)  
- **Database:** [MongoDB Atlas](https://www.mongodb.com/atlas/database) (Free Tier)  

**Deploy Your Own**

See the [Deployment Guide](docs/deployment.md) for detailed instructions on deploying to Render.

---

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app
```

---

## 👤 Author

Pranav Sarotra

[![GitHub](https://img.shields.io/badge/GitHub-000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/pranav-sarotra)  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pranavsarotra/)

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework  
- [MongoDB](https://www.mongodb.com/) - NoSQL database  
- [Pydantic](https://docs.pydantic.dev/) - Data validation library  
- [Render](https://render.com/) - Cloud hosting platform  
```
