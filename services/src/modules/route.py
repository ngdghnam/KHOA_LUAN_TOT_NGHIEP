from fastapi import FastAPI
from .user.user_controller import router as user_router
from .role.role_controller import router as role_router
from .file.file_controller import router as file_router
from .auth.auth_controller import router as auth_router

def register_routes(app: FastAPI):
    app.include_router(user_router)
    app.include_router(role_router)
    app.include_router(file_router)
    app.include_router(auth_router)