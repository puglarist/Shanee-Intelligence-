from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from fastapi.security import HTTPBearer
from datetime import timedelta
from auth import create_access_token, verify_token, get_user, User
from models import (
    UserCreate, UserResponse, TokenRequest, TokenResponse,
    FileUploadRequest, FileResponse, ComputeJobRequest, ComputeJobResponse,
    SystemStatusResponse
)
from storage import get_storage_backend, get_file_checksum, FileMetadata
from datetime import datetime
import uuid

router = APIRouter()
security = HTTPBearer()

async def get_current_user(credentials = Depends(security)):
    token = credentials.credentials
    token_data = verify_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user(token_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/auth/token", response_model=TokenResponse)
async def login(request: TokenRequest):
    if request.username != "admin" or request.password != "admin":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user = get_user(request.username) or User(username="admin", email="admin@localhost")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return TokenResponse(access_token=access_token, expires_in=1800)

@router.get("/api/user/me", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_user)):
    return UserResponse(
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active
    )

@router.post("/api/files/upload", response_model=FileResponse)
async def upload_file(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    file_id = str(uuid.uuid4())
    checksum = get_file_checksum(content)

    metadata = FileMetadata(
        file_id=file_id,
        filename=file.filename or "unknown",
        size=len(content),
        created_at=datetime.utcnow(),
        checksum=checksum,
        encrypted=False
    )

    storage = get_storage_backend()
    success = await storage.upload(file_id, content, metadata)

    if not success:
        raise HTTPException(status_code=500, detail="File upload failed")

    return FileResponse(
        file_id=file_id,
        filename=metadata.filename,
        size=metadata.size,
        created_at=metadata.created_at,
        checksum=checksum,
        encrypted=False
    )

@router.get("/api/files/{file_id}")
async def download_file(file_id: str, current_user = Depends(get_current_user)):
    storage = get_storage_backend()
    content = await storage.download(file_id)

    if not content:
        raise HTTPException(status_code=404, detail="File not found")

    return {
        "file_id": file_id,
        "content": content,
        "size": len(content)
    }

@router.delete("/api/files/{file_id}")
async def delete_file(file_id: str, current_user = Depends(get_current_user)):
    storage = get_storage_backend()
    success = await storage.delete(file_id)

    if not success:
        raise HTTPException(status_code=404, detail="File not found")

    return {"message": "File deleted successfully"}

@router.post("/api/compute/submit", response_model=ComputeJobResponse)
async def submit_compute_job(
    request: ComputeJobRequest,
    current_user = Depends(get_current_user)
):
    job_id = str(uuid.uuid4())

    # TODO: Integrate with Runpod/GPU backend
    return ComputeJobResponse(
        job_id=job_id,
        job_name=request.job_name,
        status="queued",
        created_at=datetime.utcnow(),
        timeout_minutes=request.timeout_minutes
    )

@router.get("/api/compute/jobs/{job_id}", response_model=ComputeJobResponse)
async def get_compute_job(job_id: str, current_user = Depends(get_current_user)):
    # TODO: Fetch from job queue/database
    return ComputeJobResponse(
        job_id=job_id,
        job_name="example-job",
        status="pending",
        created_at=datetime.utcnow()
    )
