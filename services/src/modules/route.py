from fastapi import FastAPI
from .user.user_controller import router as user_router
from .role.role_controller import router as role_router
from .file.file_controller import router as file_router
from .auth.auth_controller import router as auth_router
from .search.search_controller import router as search_router
from .ai_models.ai_models_controller import router as ai_router
from .cv_session.cv_session_controller import router as cv_session_router

def register_routes(app: FastAPI):
    app.include_router(user_router)
    app.include_router(role_router)
    app.include_router(file_router)
    app.include_router(auth_router)
    app.include_router(search_router)
    app.include_router(ai_router)
    app.include_router(cv_session_router)