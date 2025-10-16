from fastapi import FastAPI, Request
from middlewares import cors_middleware
from middlewares import logging_middleware
from middlewares import sql_injection_middleware

app: FastAPI = FastAPI()

info: dict = {
    "members": [
        {"name": "Nguyễn Đặng Hoài Nam", "role": "Full Stack Developer"},
        {"name": "Nguyễn Xuân Quỳnh", "role": "Project Manager"},
        {"name": "Trần Xuân Hương", "role": "Designer"},
        {"name": "Trần Xuân Hương", "role": "Designer"},
        {"name": "Nguyễn Hoàng Hương Giang", "role": "Business Analyst"},
        {"name": "Lưu Hà Vy", "role": "Product Owner"},
    ],
    "Version": "1.0.0"
}

cors_middleware.add(app)
logging_middleware.add(app)
sql_injection_middleware.add(app)
    
@app.get("/")
def readRoot(request: Request): 
    return {"message": "Welcome to my website", "Information": info}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)