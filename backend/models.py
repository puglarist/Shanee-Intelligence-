from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: str = Field(..., min_length=8, max_length=100)

class UserResponse(BaseModel):
    username: str
    email: Optional[str]
    is_active: bool
    created_at: Optional[datetime] = None

class TokenRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 1800

class FileUploadRequest(BaseModel):
    filename: str = Field(..., max_length=255)
    encrypted: bool = False

class FileResponse(BaseModel):
    file_id: str
    filename: str
    size: int
    created_at: datetime
    checksum: str
    encrypted: bool

class ComputeJobRequest(BaseModel):
    job_name: str = Field(..., max_length=255)
    job_type: str = Field(..., max_length=50)
    params: dict = Field(default_factory=dict)
    timeout_minutes: int = Field(default=30, ge=1, le=480)

class ComputeJobResponse(BaseModel):
    job_id: str
    job_name: str
    status: str
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[dict] = None

class SystemStatusResponse(BaseModel):
    api_online: bool
    gpu_available: bool
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
