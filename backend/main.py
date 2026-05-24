from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from .models import SystemStatusResponse

app = FastAPI(title="Shanee Intelligence API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def root():
    return {
        "message": "Shanee Intelligence API",
        "version": "0.1.0",
        "status": "online"
    }

@app.get("/status", response_model=SystemStatusResponse)
async def get_status():
    return SystemStatusResponse(
        api_online=True,
        gpu_available=False,
        message="System online. GPU integration coming soon."
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
