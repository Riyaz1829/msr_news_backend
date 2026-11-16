# MSR News Backend

A REST API backend for the MSR News application, built using Python and FastAPI.

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT Authentication
- Password Hashing

## Project Structure

```text
msr_news_backend/
├── app/
│   ├── core/
│   ├── database/
│   ├── modules/
│   │   ├── auth/
│   │   └── users/
│   └── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Features

- User registration
- User login
- JWT authentication
- User profile management
- Change password
- Forgot password
- Reset password

## Installation

Clone the repository:

```bash
git clone https://github.com/srinidh2002/msr_news_backend.git
cd msr_news_backend
```

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python -m uvicorn app.main:app --reload
```

## API Documentation

After starting the server, open:

http://127.0.0.1:8000/docs

## Repository

https://github.com/srinidh2002/msr_news_backend