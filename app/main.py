from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.benchmark.runner import BenchmarkRunner
from app.benchmark.report import BenchmarkReportGenerator
from app.dashboard.api import router as dashboard_router
from app.judge.languages import LANGUAGES
from app.utils.logger import configure_logger
from app.utils.config import AppConfig

app = FastAPI(title="NEO BENCHLAB")
app.include_router(dashboard_router)
logger = configure_logger()
config = AppConfig()

runner = BenchmarkRunner(config=config)
reporter = BenchmarkReportGenerator(config=config)

@app.get("/stats")
async def get_stats() -> dict:
    """Return current system statistics."""
    return runner.collect_system_stats()

@app.get("/benchmarks")
async def get_benchmarks() -> dict:
    """Return available benchmark definitions."""
    return {
        "languages": list(LANGUAGES.keys()),
        "features": [
            "compile",
            "run",
            "stress",
            "profiling",
            "reporting",
        ],
    }

@app.post("/benchmark/run")
async def run_benchmark(language: str, source: str) -> JSONResponse:
    """Run a benchmark for a submitted source file."""
    if language not in LANGUAGES:
        raise HTTPException(status_code=400, detail="Unsupported language")

    result = await runner.run_submission(language=language, source=source)
    report = reporter.generate(result)
    return JSONResponse(content=report)

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
