import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 이 줄 추가
from typing import List

app = FastAPI(
    title="My FastAPI App",
    description="FastAPI 기본 셋팅",
    version="1.0.0"
)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# CORS 미들웨어 추가 (이 부분을 추가하거나 수정)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

def get_allowed_origins() -> List[str]:
    """허용된 도메인 목록을 반환"""
    base_origins = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000"
    ]

@app.get("/cors-info")
async def cors_info():
    return {
        "allowed_origins": origins,
        "credentials_allowed": True,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "headers": "All headers allowed"
    }

@app.get("/")
async def root():
    return {"message": "CORS configured dynamically"}

# Preflight 요청 처리 (OPTIONS)
@app.options("/{path:path}")
async def options_handler(path: str):
    return {"message": "Preflight OK"}

@app.get("/")
async def root():
    return {"message": "Hello FastAPI!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React 개발 서버
        "http://localhost:8080",  # Vue.js 개발 서버
        "http://127.0.0.1:3000",
        "https://yourdomain.com",  # 실제 프로덕션 도메인
        "https://www.yourdomain.com"
    ],
    allow_credentials=True,  # 쿠키나 인증 헤더 허용
    allow_methods=[
        "GET", 
        "POST", 
        "PUT", 
        "DELETE", 
        "OPTIONS", 
        "PATCH"
    ],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",  # JWT 토큰용
        "X-Requested-With"
    ],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/protected")
async def protected_data():
    return {"data": "This requires CORS"}

if ENVIRONMENT == "development":
    # 개발 환경: 모든 도메인 허용
    origins = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:5173",  # Vite
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:5173"
    ]
elif ENVIRONMENT == "staging":
    # 스테이징 환경
    origins = [
        "https://staging.yourdomain.com",
        "https://test.yourdomain.com"
    ]
else:
    # 프로덕션 환경
    origins = [
        "https://yourdomain.com",
        "https://www.yourdomain.com"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Hello World", 
        "environment": ENVIRONMENT,
        "allowed_origins": origins
    }

@app.get("/api/cors-test")
async def cors_test():
    return {"cors": "enabled", "message": "CORS is working!"}