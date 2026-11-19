from fastapi import FastAPI

from app.database.base import Base
from app.database.session import engine

from app.modules.users import models
from app.modules.auth.routes import router as auth_router, otp_router
from app.modules.users.router import router as users_router
from app.modules.mock.routes import router as mock_router

app = FastAPI(
    title="MSR News Backend",
    description="User Registration API",
    version="1.0.0"
)


# Create database tables
Base.metadata.create_all(bind=engine)


# Register authentication routes
app.include_router(auth_router)
app.include_router(otp_router)
app.include_router(users_router)
app.include_router(mock_router)


# @app.get("/")
# def home():

#     return {
#         "message": "MSR News Backend API is running"
#     }