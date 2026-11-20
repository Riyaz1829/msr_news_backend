# MSR News Backend

Backend API for the MSR News Channel hyperlocal Telugu news application, built using FastAPI and Python.

## 1. Technology Stack

- **Backend Framework:** FastAPI
- **Programming Language:** Python
- **Database ORM:** SQLAlchemy
- **Authentication:** JWT (HS256)
- **Password Hashing:** Argon2
- **Cache and Rate Limiting:** Redis
- **Database Migrations:** Alembic
- **API Documentation:** Swagger UI

## 2. Project Structure

```text
msr_news_backend/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── redis.py
│   │   └── security.py
│   │
│   ├── database/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── async_session.py
│   │
│   ├── modules/
│   │   ├── auth/
│   │   ├── users/
│   │   ├── reporters/
│   │   ├── locations/
│   │   ├── kyc/
│   │   ├── community/
│   │   ├── notifications/
│   │   └── mock/
│   │
│   ├── schemas/
│   └── services/
│       ├── cache.py
│       ├── email_service.py
│       ├── msg91.py
│       └── rate_limit.py
│
├── tests/
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## 3. Setup Instructions

### Prerequisites

- Python installed
- Redis installed or running through Docker
- Git

### Clone the repository

```bash
git clone <your-repository-url>
cd msr_news_backend
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Environment Configuration

Create a `.env` file in the project root.

```env
SECRET_KEY=your_secret_key
REDIS_URL=redis://localhost:6379/0
```

Use a strong, private secret key. Never commit `.env` or expose credentials in GitHub.

## 5. Start Redis

If using Docker:

```bash
docker start msr-redis
```

Check the Redis connection:

```bash
docker exec -it msr-redis redis-cli ping
```

Expected response:

```text
PONG
```

## 6. Run the Backend

From the project root:

```bash
python -m uvicorn app.main:app --reload
```

Backend server:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

Alternative API documentation:

```text
http://127.0.0.1:8000/redoc
```

## 7. Current Backend Modules

| Module | Purpose |
|---|---|
| Auth | User registration and login |
| Users | User-related operations and password reset |
| Reporters | Reporter-related module |
| Locations | Location-related module |
| KYC | Identity verification module |
| Community | Community-related module |
| Notifications | Notification-related module |
| Mock | Mock home feed endpoint |

The presence of a module in the project structure does not necessarily mean all its functionality is complete.

## 8. Supporting Services

- **Redis Cache:** Provides reusable cache operations with TTL support.
- **Rate Limiting:** Redis-based OTP request rate limiting.
- **Email Service:** Mock password-reset email service for development.
- **MSG91 Service:** Mock OTP dispatch service for development.

Mock services simulate provider responses. They do not deliver real emails or SMS messages.

## 9. Running Backend Tests

Run the test modules from the project root:

```bash
python -m tests.test_redis
python -m tests.test_cache
python -m tests.test_cache_ttl
python -m tests.test_msg91
python -m tests.test_rate_limit
```

These tests cover Redis connectivity, cache operations, TTL expiry, mock MSG91 behavior, and OTP rate limiting.

## 10. Development Notes

- Keep sensitive credentials inside `.env`.
- Do not commit virtual environments, database files, or Python cache files.
- Coordinate database schema changes with the database team.
- Real OTP and email provider integration requires approved credentials and configuration.
- Verify unfinished modules before treating them as production-ready.

## 11. API Development

The backend uses FastAPI routers to organize endpoints by module.

New endpoints should follow the existing module structure and separate route handling, validation, and business logic where appropriate.

---

**Project:** MSR News Channel  
**Component:** Backend API  
**Framework:** FastAPI  
**Documentation Status:** Development documentation