"""
HarvestSaarthi AI - Main FastAPI Application
Entrypoint for the decision support agent API.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import sys
import os

# Ensure backend directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.api.router import router as api_router

app = FastAPI(
    title="HarvestSaarthi AI Agent",
    description="Evidence-driven AI decision agent for rural Bharat post-harvest decisions.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS setup for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hackathon permissive CORS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router)

# Locate frontend/dist directory relative to backend or CWD
frontend_dist_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))

if os.path.exists(frontend_dist_path):
    assets_path = os.path.join(frontend_dist_path, "assets")
    if os.path.exists(assets_path):
        app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("redoc") or full_path == "openapi.json":
            raise HTTPException(status_code=404, detail="Not Found")

        target_file = os.path.join(frontend_dist_path, full_path)
        if full_path and os.path.isfile(target_file):
            return FileResponse(target_file)

        index_file = os.path.join(frontend_dist_path, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return JSONResponse({"message": "HarvestSaarthi AI Decision Agent API is running."})
else:
    @app.get("/")
    def root():
        return {
            "message": "HarvestSaarthi AI Decision Agent API is running.",
            "tagline": "From Harvest Uncertainty to the Right Next Move.",
            "health_check": "/api/health",
            "documentation": "/docs",
        }


@app.exception_handler(Exception)
def global_exception_handler(request, exc):
    """Zero-crash fallback exception handler."""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "data": None,
            "error": f"Internal Agent Exception: {str(exc)}",
        },
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
