import re
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import json


class SQLInjectionMiddleware(BaseHTTPMiddleware):
    """
    Middleware để phát hiện và chặn các mẫu SQL injection phổ biến
    """
    
    # Các mẫu SQL injection phổ biến
    SQL_INJECTION_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE|UNION|DECLARE)\b)",
        r"(--|\#|\/\*|\*\/)",  # SQL comments
        r"('\s*(OR|AND)\s*'?\d*'?\s*=\s*'?\d*)",  # OR 1=1, AND 1=1
        r"('\s*(OR|AND)\s*\w+\s*=\s*\w+)",  # OR 'a'='a'
        r"(;\s*(DROP|DELETE|UPDATE|INSERT))",  # Stacked queries
        r"(WAITFOR\s+DELAY)",  # Time-based attacks
        r"(SLEEP\s*\()",  # MySQL sleep
        r"(BENCHMARK\s*\()",  # MySQL benchmark
        r"(LOAD_FILE\s*\()",  # File reading
        r"(INTO\s+(OUT|DUMP)FILE)",  # File writing
        r"(\bxp_\w+)",  # SQL Server extended procedures
        r"(;\s*SHUTDOWN)",  # Shutdown commands
    ]
    
    def __init__(self, app, check_query_params: bool = True, 
                 check_body: bool = True, check_headers: bool = False):
        super().__init__(app)
        self.check_query_params = check_query_params
        self.check_body = check_body
        self.check_headers = check_headers
        self.compiled_patterns = [
            re.compile(pattern, re.IGNORECASE) for pattern in self.SQL_INJECTION_PATTERNS
        ]
    
    def _contains_sql_injection(self, text: str) -> bool:
        """Kiểm tra xem text có chứa mẫu SQL injection không"""
        if not text:
            return False
        
        # Decode URL encoding nếu có
        try:
            from urllib.parse import unquote
            decoded_text = unquote(text)
        except:
            decoded_text = text
        
        # Kiểm tra với từng pattern
        for pattern in self.compiled_patterns:
            if pattern.search(decoded_text):
                return True
        return False
    
    def _check_dict(self, data: dict, path: str = "") -> tuple[bool, str]:
        """Kiểm tra dictionary đệ quy để tìm SQL injection"""
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            
            # Kiểm tra key
            if self._contains_sql_injection(str(key)):
                return True, f"Key: {current_path}"
            
            # Kiểm tra value
            if isinstance(value, str):
                if self._contains_sql_injection(value):
                    return True, f"Value at {current_path}"
            elif isinstance(value, dict):
                found, location = self._check_dict(value, current_path)
                if found:
                    return True, location
            elif isinstance(value, list):
                for idx, item in enumerate(value):
                    if isinstance(item, str):
                        if self._contains_sql_injection(item):
                            return True, f"{current_path}[{idx}]"
                    elif isinstance(item, dict):
                        found, location = self._check_dict(item, f"{current_path}[{idx}]")
                        if found:
                            return True, location
        return False, ""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Kiểm tra query parameters
        if self.check_query_params:
            for key, value in request.query_params.items():
                if self._contains_sql_injection(key) or self._contains_sql_injection(value):
                    return JSONResponse(
                        status_code=400,
                        content={
                            "error": "Potential SQL injection detected in query parameters",
                            "message": "Your request contains suspicious patterns"
                        }
                    )
        
        # Kiểm tra headers (tùy chọn)
        if self.check_headers:
            for key, value in request.headers.items():
                if self._contains_sql_injection(value):
                    return JSONResponse(
                        status_code=400,
                        content={
                            "error": "Potential SQL injection detected in headers",
                            "message": "Your request contains suspicious patterns"
                        }
                    )
        
        # Kiểm tra request body
        if self.check_body and request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if body:
                    # Lưu lại body để các handler sau có thể sử dụng
                    async def receive():
                        return {"type": "http.request", "body": body}
                    request._receive = receive
                    
                    # Parse JSON body
                    try:
                        body_str = body.decode("utf-8")
                        body_json = json.loads(body_str)
                        
                        if isinstance(body_json, dict):
                            found, location = self._check_dict(body_json)
                            if found:
                                return JSONResponse(
                                    status_code=400,
                                    content={
                                        "error": "Potential SQL injection detected in request body",
                                        "location": location,
                                        "message": "Your request contains suspicious patterns"
                                    }
                                )
                        elif isinstance(body_json, str):
                            if self._contains_sql_injection(body_json):
                                return JSONResponse(
                                    status_code=400,
                                    content={
                                        "error": "Potential SQL injection detected in request body",
                                        "message": "Your request contains suspicious patterns"
                                    }
                                )
                    except json.JSONDecodeError:
                        # Nếu không phải JSON, kiểm tra như string
                        if self._contains_sql_injection(body_str):
                            return JSONResponse(
                                status_code=400,
                                content={
                                    "error": "Potential SQL injection detected in request body",
                                    "message": "Your request contains suspicious patterns"
                                }
                            )
            except Exception as e:
                pass  # Nếu không đọc được body, bỏ qua
        
        # Tiếp tục xử lý request
        response = await call_next(request)
        return response


def add(app: FastAPI, 
        check_query_params: bool = True, 
        check_body: bool = True, 
        check_headers: bool = False):
    """
    Thêm SQL Injection Prevention Middleware vào FastAPI app
    
    Args:
        app: FastAPI application instance
        check_query_params: Kiểm tra query parameters (mặc định: True)
        check_body: Kiểm tra request body (mặc định: True)
        check_headers: Kiểm tra headers (mặc định: False)
    
    Example:
        from sql_injection_middleware import add as add_sql_injection_middleware
        
        app = FastAPI()
        add_sql_injection_middleware(app)
    """
    app.add_middleware(
        SQLInjectionMiddleware,
        check_query_params=check_query_params,
        check_body=check_body,
        check_headers=check_headers
    )