from abc import ABC, abstractmethod
from typing import Optional
import os
import hashlib
from datetime import datetime
from pydantic import BaseModel

class FileMetadata(BaseModel):
    file_id: str
    filename: str
    size: int
    created_at: datetime
    checksum: str
    encrypted: bool

class StorageBackend(ABC):
    @abstractmethod
    async def upload(self, file_id: str, content: bytes, metadata: FileMetadata) -> bool:
        pass

    @abstractmethod
    async def download(self, file_id: str) -> Optional[bytes]:
        pass

    @abstractmethod
    async def delete(self, file_id: str) -> bool:
        pass

    @abstractmethod
    async def list_files(self, user_id: str) -> list[FileMetadata]:
        pass

class LocalStorageBackend(StorageBackend):
    def __init__(self, base_path: str = "/tmp/shanee-storage"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    async def upload(self, file_id: str, content: bytes, metadata: FileMetadata) -> bool:
        try:
            file_path = os.path.join(self.base_path, file_id)
            with open(file_path, "wb") as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Upload error: {e}")
            return False

    async def download(self, file_id: str) -> Optional[bytes]:
        try:
            file_path = os.path.join(self.base_path, file_id)
            with open(file_path, "rb") as f:
                return f.read()
        except FileNotFoundError:
            return None

    async def delete(self, file_id: str) -> bool:
        try:
            file_path = os.path.join(self.base_path, file_id)
            os.remove(file_path)
            return True
        except FileNotFoundError:
            return False

    async def list_files(self, user_id: str) -> list[FileMetadata]:
        # This will be enhanced in Phase 2 with database-backed file listing
        return []

def get_file_checksum(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()

def get_storage_backend(backend_type: str = "local") -> StorageBackend:
    if backend_type == "local":
        return LocalStorageBackend()
    else:
        raise ValueError(f"Unknown storage backend: {backend_type}")
