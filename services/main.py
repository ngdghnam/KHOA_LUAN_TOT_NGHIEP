from fastapi import FastAPI, Request
from src.middlewares import cors_middleware, logging_middleware, sql_injection_middleware
from src.modules.route import register_routes
from src.exceptions.exception import custom_exception_handler
from fastapi import HTTPException
from src.config.lifespan import lifespan
from src.config.minio_config import minio_config

info: dict = {
    "version": "1.0.0",
    "author": "Nguyễn Đặng Hoài Nam"
}

app: FastAPI = FastAPI(lifespan=lifespan)

# Middlewares
cors_middleware.add(app)
logging_middleware.add(app)
sql_injection_middleware.add(app)
    
@app.get("/")
def readRoot(request: Request): 
    return {"message": "Welcome to our website", "Information": info}

# Routes
register_routes(app=app)

# minio
minio_config.connect()

# Exception
app.add_exception_handler(HTTPException, custom_exception_handler)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=5000, reload=True)