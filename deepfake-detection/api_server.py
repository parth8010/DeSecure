"""
FastAPI REST API Server for Advanced Deepfake Detection
"""

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import tempfile
import os
import uvicorn
import logging

logger = logging.getLogger(__name__)

def start_server(detector, host="0.0.0.0", port=8000):
    """
    Start FastAPI server with deepfake detection endpoints
    """
    app = FastAPI(
        title="Advanced Deepfake Detection API",
        description="REST API for video & image deepfake detection",
        version="1.0.0"
    )

    @app.get("/")
    def root():
        return {
            "status": "running",
            "service": "Advanced Deepfake Detection API"
        }

    @app.post("/analyze/image")
    async def analyze_image(file: UploadFile = File(...)):
        """
        Analyze an uploaded image for deepfakes
        """
        try:
            # Save uploaded image temporarily
            suffix = os.path.splitext(file.filename)[-1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(await file.read())
                tmp_path = tmp.name

            # Run detection
            results = detector.analyze_image(tmp_path)

            # Cleanup
            os.unlink(tmp_path)

            return JSONResponse(content=results)

        except Exception as e:
            logger.error(f"Image analysis failed: {e}")
            return JSONResponse(
                status_code=500,
                content={"success": False, "error": str(e)}
            )

    @app.post("/analyze/video")
    async def analyze_video(file: UploadFile = File(...)):
        """
        Analyze an uploaded video for deepfakes
        """
        try:
            # Save uploaded video temporarily
            suffix = os.path.splitext(file.filename)[-1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(await file.read())
                tmp_path = tmp.name

            # Run detection
            results = detector.analyze_video(tmp_path)

            # Cleanup
            os.unlink(tmp_path)

            return JSONResponse(content=results)

        except Exception as e:
            logger.error(f"Video analysis failed: {e}")
            return JSONResponse(
                status_code=500,
                content={"success": False, "error": str(e)}
            )

    @app.get("/health")
    def health_check():
        return {
            "status": "healthy",
            "gpu_available": detector.device.type == "cuda"
        }

    logger.info(f"Starting API server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
