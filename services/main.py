from fastapi import FastAPI, Request
from src.middlewares import cors_middleware, logging_middleware, sql_injection_middleware
from src.database.database import database
from src.modules.route import register_routes

app: FastAPI = FastAPI()

info: dict = {
    "version": "1.0.0",
    "author": "Nguyễn Đặng Hoài Nam"
}

# Middlewares
cors_middleware.add(app)
logging_middleware.add(app)
sql_injection_middleware.add(app)

# Database connection
@app.on_event("startup")
async def startup():
    await database.check_connection()
    
@app.get("/")
def readRoot(request: Request): 
    return {"message": "Welcome to our website", "Information": info}

register_routes(app=app)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=5000, reload=True)