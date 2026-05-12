from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.benchmark.runner import BenchmarkRunner
from app.benchmark.report import BenchmarkReportGenerator
from app.dashboard.api import router as dashboard_router
from app.judge.languages import LANGUAGES
from app.utils.logger import configure_logger
from app.utils.config import AppConfig
import time
import json

class BenchmarkRequest(BaseModel):
    language: str
    source: str

app = FastAPI(
    title="NEO BENCHLAB",
    version="1.0.0",
    description="Professional Benchmark & Performance Analysis Platform for Online Judge Systems"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router)
logger = configure_logger()
config = AppConfig()

runner = BenchmarkRunner(config=config)
reporter = BenchmarkReportGenerator(config=config)

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("NEO BENCHLAB starting up...")
    logger.info(f"Configuration: stress_test={config.enable_stress_test}, threads={config.threads}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("NEO BENCHLAB shutting down...")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add request processing time to response headers."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.debug(f"{request.method} {request.url.path} - {process_time:.4f}s")
    return response

@app.get("/stats")
async def get_stats() -> dict:
    """Return current system statistics."""
    return runner.collect_system_stats()

@app.get("/benchmarks")
async def get_benchmarks() -> dict:
    """Return available benchmark definitions."""
    logger.debug("Fetching available benchmarks")
    return {
        "languages": list(LANGUAGES.keys()),
        "features": [
            "compile",
            "run",
            "stress",
            "profiling",
            "reporting",
        ],
        "config": {
            "stress_test_enabled": config.enable_stress_test,
            "threads": config.threads,
            "stress_requests": config.stress_requests,
            "timeout_seconds": config.timeout_seconds,
        }
    }

@app.post("/benchmark/run")
async def run_benchmark(req: BenchmarkRequest) -> JSONResponse:
    """Run a benchmark for a submitted source file."""
    if req.language not in LANGUAGES:
        raise HTTPException(status_code=400, detail="Unsupported language")

    try:
        result = await runner.run_submission(language=req.language, source=req.source)
        report = reporter.generate(result)
        return JSONResponse(content=report)
    except Exception as e:
        logger.error(f"Benchmark error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reports")
async def list_reports() -> dict:
    """List recent report metadata."""
    return reporter.list_reports()

@app.get("/system/health")
async def system_health() -> dict:
    """Return basic health data for the service."""
    return {
        "status": "ok",
        "uptime_seconds": runner.get_uptime_seconds(),
    }
