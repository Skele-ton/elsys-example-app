from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
import inspect
import logging
import os
from pathlib import Path
from datetime import datetime
from functools import wraps
from time import perf_counter

app = FastAPI(title="File Storage API", version="1.0.0")

# Directory where files will be stored
STORAGE_DIR = Path("storage")
STORAGE_DIR.mkdir(exist_ok=True)
logger = logging.getLogger("storage_api")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


def log_endpoint(action: str):
    """
    Decorator (Decorator Pattern) that logs execution time of endpoints.
    """
    def decorator(func):
        if not inspect.iscoroutinefunction(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = perf_counter()
                try:
                    return func(*args, **kwargs)
                finally:
                    duration_ms = (perf_counter() - start) * 1000
                    logger.info("%s completed in %.2f ms", action, duration_ms)
            return wrapper

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = perf_counter()
            try:
                return await func(*args, **kwargs)
            finally:
                duration_ms = (perf_counter() - start) * 1000
                logger.info("%s completed in %.2f ms", action, duration_ms)

        return async_wrapper

    return decorator

# Counter for files stored (initialize with existing files count)
def get_file_count():
    return len([f for f in STORAGE_DIR.iterdir() if f.is_file()])

files_stored_counter = get_file_count()


@app.get("/")
async def root():
    return {
        "message": "File Storage API",
        "endpoints": [
            "GET /files/{filename}",
            "POST /files",
            "GET /files",
            "GET /health",
            "GET /metrics"
        ]
    }


@app.get("/files/{filename}")
@log_endpoint("get_file")
async def get_file(filename: str):
    """
    Retrieve a file by filename.
    
    Args:
        filename: Name of the file to retrieve
        
    Returns:
        FileResponse with the requested file
        
    Raises:
        HTTPException: If file is not found
    """
    file_path = STORAGE_DIR / filename
    
    # Security check: prevent directory traversal
    if not file_path.resolve().is_relative_to(STORAGE_DIR.resolve()):
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )


@app.post("/files")
@log_endpoint("store_file")
async def store_file(file: UploadFile = File(...)):
    """
    Store a file locally on the filesystem.
    
    Args:
        file: The file to upload
        
    Returns:
        JSON response with file information
        
    Raises:
        HTTPException: If file storage fails
    """
    try:
        # Security check: prevent directory traversal in filename
        filename = os.path.basename(file.filename)
        if not filename or filename in (".", ".."):
            raise HTTPException(status_code=400, detail="Invalid filename")
        
        file_path = STORAGE_DIR / filename
        
        # Read file content
        content = await file.read()
        
        # Write file to storage directory
        file_exists = file_path.exists()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Increment counter only if it's a new file
        global files_stored_counter
        if not file_exists:
            files_stored_counter += 1
        
        return {
            "message": "File stored successfully",
            "filename": filename,
            "size": len(content),
            "content_type": file.content_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store file: {str(e)}")


@app.get("/files")
@log_endpoint("list_files")
async def list_files():
    """
    List all stored files.
    
    Returns:
        JSON response with list of filenames
    """
    files = [f.name for f in STORAGE_DIR.iterdir() if f.is_file()]
    return {"files": files, "count": len(files)}


@app.get("/health")
@log_endpoint("health_check")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        JSON response indicating server health status
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "File Storage API"
    }


@app.get("/metrics")
@log_endpoint("metrics")
async def metrics():
    """
    Metrics endpoint providing server statistics.
    
    Returns:
        JSON response with various metrics
    """
    files = [f for f in STORAGE_DIR.iterdir() if f.is_file()]
    total_size = sum(f.stat().st_size for f in files)
    
    return {
        "files_stored_total": files_stored_counter,
        "files_current": len(files),
        "total_storage_bytes": total_size,
        "total_storage_mb": round(total_size / (1024 * 1024), 2),
        "timestamp": datetime.utcnow().isoformat()
    }

