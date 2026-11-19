
# MSR News Backend

A REST API backend for the MSR News application, a hyperlocal Telugu news platform. Built using Python and FastAPI.

## About the Project

MSR News aims to deliver local news updates to users based on their locations.

The backend provides APIs for authentication, user management, news feeds, OTP services, password recovery, caching, and other platform features.

## Technologies Used

- Python 3.13
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL (planned production database)
- SQLite (current local database setup)
- Redis
- JWT Authentication
- Password Hashing
- Docker (Redis development setup)

## Project Structure

```text
msr_news_backend/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── redis.py
│   │   └── security.py
│   │
│   ├── database/
│   │   ├── async_session.py
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── modules/
│   │   ├── auth/
│   │   ├── community/
│   │   ├── kyc/
│   │   ├── locations/
│   │   ├── mock/
│   │   ├── notifications/
│   │   ├── reporters/
│   │   └── users/
│   │
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Features Implemented

### Authentication
- User registration
- Login using email or mobile number
- JWT access token generation
- Password hashing and verification
- Forgot password functionality
- Password reset using JWT reset tokens
- Password confirmation validation

### OTP Services
- Mock OTP sending service
- Mobile number validation
- Six-digit OTP generation
- Redis-based rate limiting
- Maximum 5 OTP requests per hour

### Email Services
- Mock password reset email service
- Development reset link generation

### Caching
- Redis connection
- Cache data storage and retrieval
- Cache deletion
- Configurable cache expiration

### Mock News Feed
- Home feed API
- Mock news articles
- Pagination support

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Riyaz1829/msr_news_backend.git
cd msr_news_backend
```

### 2. Create Virtual Environment

Windows:

```powershell
python -m venv venv
```

### 3. Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root.

Add the required configuration values:

```env
SECRET_KEY=your-secret-key
ALGORITHM=HS256
DATABASE_URL=your-database-url
REDIS_URL=redis://localhost:6379/0
```

Use your own secure development values. Never commit `.env` to GitHub.

### 6. Start Redis

If using the existing Docker container:

```bash
docker start msr-redis
```

Verify Redis:

```bash
docker exec -it msr-redis redis-cli ping
```

Expected output:

```text
PONG
```

### 7. Run FastAPI

```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server starts, access:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Authentication API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /auth/register | User registration |
| POST | /auth/login | Login using email or mobile |
| POST | /users/forgot-password | Request password reset |
| POST | /users/reset-password | Reset password |

## OTP API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/v1/auth/otp/send | Send mock OTP |

Note: OTP verification is not implemented yet.

## Development Status

- Authentication APIs: Implemented and tested
- Password recovery: Implemented and tested with mock email
- OTP sending: Mock implementation tested
- Redis rate limiting: Implemented and tested
- Redis caching: Implemented and tested
- News feed: Mock implementation available
- Google Login: Planned
- Real email delivery: Pending provider configuration
- Real SMS delivery: Pending MSG91 credentials and approved DLT configuration
- Production database integration: Pending database team integration

## Security Notes

- Passwords are hashed before storage.
- JWT tokens are used for authentication.
- Environment variables are used for sensitive configuration.
- Mock email and OTP services are for development only.
- Mock authentication must not be used in production.

## Repository

GitHub: https://github.com/Riyaz1829/msr_news_backend

## License

Internal project – MSR News.
