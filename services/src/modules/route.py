from fastapi import FastAPI
from .user.user_controller import router as user_router

def register_routes(app: FastAPI):
    app.include_router(user_router)