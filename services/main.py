from fastapi import FastAPI, Request
from src.middlewares import cors_middleware, logging_middleware, sql_injection_middleware
from src.modules.route import register_routes
from src.exceptions.exception import custom_exception_handler
from fastapi import HTTPException
from src.config.lifespan import lifespan
from src.config.minio_config import minio_config

desc: str = "This Platform is designed to scan and analyse CVs automatically by AI. \n" \
"After scanning and analyzing, the system will generate keywords and then search google to find information or courses to " \
"improve the CVs"

info: dict = {
    "version": "1.0.0",
    "author": "Nguyễn Đặng Hoài Nam",
    "description": desc
}

app: FastAPI = FastAPI(lifespan=lifespan)

# Middlewares
cors_middleware.add(app)
logging_middleware.add(app)
# sql_injection_middleware.add(app)
    
@app.get("/")
def readRoot(request: Request): 
    print("request", request)
    return {
        "message": "Welcome to Scan & Analyze CV Automation Platform", 
        "Information": info
    }

# Routes
register_routes(app=app)

# minio
minio_config.connect()

# Exception
app.add_exception_handler(HTTPException, custom_exception_handler)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=5000, reload=True)