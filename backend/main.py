from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from typing import Optional
import os

app = FastAPI(title="Shanee Intelligence API", version="0.1.0")

# CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Models
class TokenRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class SystemStatus(BaseModel):
    api_online: bool
    gpu_available: bool
    message: str

# Helper functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Routes
@app.get("/")
async def root():
    return {
        "message": "Shanee Intelligence API",
        "version": "0.1.0",
        "status": "online"
    }

@app.get("/status", response_model=SystemStatus)
async def get_status():
    return SystemStatus(
        api_online=True,
        gpu_available=False,  # Will detect actual GPU availability later
        message="System online. GPU integration coming soon."
    )

@app.post("/auth/token", response_model=TokenResponse)
async def login(request: TokenRequest):
    # Simple authentication for MVP (replace with proper auth)
    if request.username == "admin" and request.password == "admin":
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": request.username},
            expires_delta=access_token_expires
        )
        return TokenResponse(access_token=access_token, token_type="bearer")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

@app.get("/api/user/me")
async def get_current_user(token: str = Depends(lambda: None)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    username = verify_token(token)
    return {"username": username}

@app.post("/api/files/upload")
async def upload_file():
    return {"message": "File upload endpoint - not yet implemented"}

@app.post("/api/compute/submit")
async def submit_job():
    return {"message": "GPU job submission - not yet implemented"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
