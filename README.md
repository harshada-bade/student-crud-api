# Student CRUD API

A REST API built with Python and Flask to manage student records.

---

## Prerequisites

- Python 3.9+
- Git

---

## Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/harshada-bade/student-crud-api.git
cd student-crud-api
```

### 2. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
make install
```

### 4. Configure environment variables
```bash
cp .env.example .env
```

Open `.env` and fill in your values:


### 5. Run database migrations
```bash
make migrate
```

### 6. Start the server
```bash
make run
```

Server runs at `http://127.0.0.1:5000`

---

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `DATABASE_URL` | Database connection URL | `sqlite:///students.db` |
| `LOG_LEVEL` | Logging level | `DEBUG` or `INFO` |

---

## How to Run Tests

```bash
make test
```

Expected output:

---

## API Endpoints

### Health Check

| Method | URL | Description |
|---|---|---|
| GET | `/healthcheck` | Check if API is running |

**Response:**
```json
{ "status": "ok" }
```

---

### Students

| Method | URL | Description | Status Code |
|---|---|---|---|
| POST | `/api/v1/students` | Create a new student | 201 |
| GET | `/api/v1/students` | Get all students | 200 |
| GET | `/api/v1/students/<id>` | Get a student by ID | 200 |
| PUT | `/api/v1/students/<id>` | Update a student | 200 |
| DELETE | `/api/v1/students/<id>` | Delete a student | 200 |

---

### Request Body — POST and PUT

```json
{
    "name": "Alice Smith",
    "email": "alice@example.com",
    "age": 20,
    "grade": "A"
}
```

| Field | Type | Required | Rules |
|---|---|---|---|
| `name` | string | yes | max 100 characters |
| `email` | string | yes | must be unique |
| `age` | integer | yes | must be a number |
| `grade` | string | yes | max 2 characters |

---

### Response Example

```json
{
    "id": 1,
    "name": "Alice Smith",
    "email": "alice@example.com",
    "age": 20,
    "grade": "A"
}
```

---

### Error Responses

| Status Code | Meaning |
|---|---|
| 400 | Missing or invalid fields |
| 404 | Student not found |
| 409 | Email already exists |
| 500 | Internal server error |

---

## Project Structure

```
student-crud-api/
├── app/
│   ├── __init__.py         ← creates the Flask app
│   ├── config.py           ← reads env vars
│   ├── models/
│   │   └── student.py      ← Student database table
│   ├── routes/
│   │   └── student.py      ← API endpoints
│   └── services/
│       └── student.py      ← business logic
├── migrations/             ← auto-generated, don't touch
├── tests/
│   ├── conftest.py         ← test setup
│   └── test_students.py    ← unit tests
├── .env                    ← local secrets, never committed
├── .env.example            ← safe template
├── .gitignore              ← ignored files
├── requirements.txt        ← project dependencies
├── Makefile                ← shortcuts for common commands
├── run.py                  ← entry point
└── README.md               ← documentation
```

---

## Makefile Commands

| Command | What it does |
|---|---|
| `make install` | Install all dependencies |
| `make run` | Start the development server |
| `make migrate` | Apply database migrations |
| `make test` | Run all tests |
