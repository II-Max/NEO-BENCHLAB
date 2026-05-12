# 🚀 NEO BENCHLAB - Quick Start Guide

## ✅ Project Status: FULLY UPGRADED & OPERATIONAL

The project has been completely assessed, fixed, and enhanced. All systems are go!

---

## 🎯 Quick Start (2 minutes)

### 1. Activate Virtual Environment
```bash
cd /home/chung/Desktop/NEO-BENCHLAB
source venv/bin/activate
```

### 2. Start the Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Test an Endpoint
In another terminal:
```bash
curl -X POST http://localhost:8000/benchmark/run \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "source": "print(\"Hello Benchmark!\")\nfor i in range(5):\n    print(i**2)"
  }'
```

---

## 📚 Available API Endpoints

### Health & Status
```bash
GET http://localhost:8000/system/health
# Returns: {"status": "ok", "uptime_seconds": ...}

GET http://localhost:8000/stats
# Returns: {"cpu_avg": ..., "cpu_peak": ..., "ram_avg_mb": ...}
```

### Benchmark Management
```bash
GET http://localhost:8000/benchmarks
# Returns: Languages, features, and configuration

GET http://localhost:8000/reports
# Returns: List of recent reports

POST http://localhost:8000/benchmark/run
# Body: {"language": "python", "source": "print('hello')"}
# Returns: Detailed benchmark results with metrics
```

### Dashboard
```bash
GET http://localhost:8000/dashboard/status
# Returns: {"status": "dashboard ready"}

WebSocket: ws://localhost:8000/dashboard/updates
# Real-time benchmark updates
```

---

## 🔧 What Was Fixed

| Issue | Solution |
|-------|----------|
| Missing dependencies | ✅ Installed all packages (fastapi, uvicorn, psutil, etc.) |
| Type hint bugs | ✅ Fixed `any` → `Any` in monitor.py |
| Broken executor calls | ✅ Added Executor instance, fixed method calls |
| Missing to_dict() methods | ✅ Added serialization for result objects |
| Incomplete modules | ✅ Enhanced profiler, charts, queue, sandbox, websocket |
| No error handling | ✅ Added comprehensive error handling & logging |
| Weak logging | ✅ Enhanced logger with detailed formatting |

---

## 🌟 What Was Enhanced

- ✨ **Profiler**: py-spy integration ready (optional)
- ✨ **Charts**: Plotly-ready visualization builder
- ✨ **Queue**: Full async task queue with statistics
- ✨ **Sandbox**: Resource limit management
- ✨ **WebSocket**: Robust real-time communication
- ✨ **Logging**: Advanced logging with line numbers
- ✨ **Middleware**: Request timing & CORS support
- ✨ **Configuration**: Runtime configuration display

---

## 📊 Sample Benchmark Request & Response

### Request
```json
POST /benchmark/run
{
  "language": "python",
  "source": "total = sum(range(1, 101))\nprint(total)"
}
```

### Response
```json
{
  "timestamp": "2026-05-12T16:47:28Z",
  "metadata": {
    "language": "python",
    "compile_success": true,
    "execution_success": true
  },
  "metrics": {
    "system": {
      "cpu_avg": 45.5,
      "cpu_peak": 92.1,
      "ram_avg_mb": 6728.6,
      "ram_peak_mb": 7042.1
    },
    "compile": {
      "success": true,
      "output": "skipped",
      "binary_path": null
    },
    "execution": {
      "success": true,
      "stdout": "5050",
      "stderr": "",
      "duration": 0.025
    }
  }
}
```

---

## 🎓 Understanding the Architecture

```
Client Request
    ↓
FastAPI (main.py)
    ↓
Routing & Validation
    ├→ /benchmark/run
    │   ↓
    │   BenchmarkRunner
    │   ├→ Compiler (language-specific compilation)
    │   ├→ Executor (code execution with temp files)
    │   ├→ SystemMonitor (CPU/memory tracking)
    │   ├→ StressTester (concurrent execution)
    │   └→ BenchmarkReportGenerator (results formatting)
    │
    ├→ /stats
    │   └→ SystemMonitor.snapshot()
    │
    └→ /benchmarks
        └→ LANGUAGES config + features
    ↓
Response (JSON)
```

---

## 🔍 Project Structure

```
NEO-BENCHLAB/
├── app/
│   ├── benchmark/          # Benchmarking engine
│   │   ├── runner.py       # Orchestration logic
│   │   ├── monitor.py      # System monitoring
│   │   ├── executor.py     # Code execution
│   │   ├── compiler.py     # Compilation logic
│   │   ├── stress.py       # Stress testing
│   │   ├── profiler.py     # Performance profiling
│   │   ├── charts.py       # Visualization builder
│   │   ├── report.py       # Report generation
│   │   └── metrics.py      # Metric aggregation
│   │
│   ├── judge/              # Code execution sandbox
│   │   ├── executor.py     # Execution engine
│   │   ├── compiler.py     # Compiler interface
│   │   ├── languages.py    # Language configs
│   │   ├── queue.py        # Task queue
│   │   └── sandbox.py      # Sandbox manager
│   │
│   ├── dashboard/          # Dashboard & WebSocket
│   │   ├── api.py          # REST endpoints
│   │   └── websocket.py    # Real-time updates
│   │
│   ├── utils/              # Shared utilities
│   │   ├── config.py       # Configuration
│   │   ├── logger.py       # Logging setup
│   │   ├── errors.py       # Custom exceptions
│   │   ├── helpers.py      # Helper functions
│   │   └── timer.py        # Timing utilities
│   │
│   └── main.py             # FastAPI entrypoint
│
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Docker Compose config
├── venv/                   # Virtual environment
└── README.md              # Documentation
```

---

## 🚦 Status Dashboard

| Component | Status | Notes |
|-----------|--------|-------|
| Compiler | ✅ Working | Supports Python, C++, Java, Node.js |
| Executor | ✅ Working | Proper temp file handling |
| Monitor | ✅ Working | CPU & memory tracking active |
| Queue | ✅ Working | Async queue with priorities |
| Sandbox | ✅ Working | Resource limits configurable |
| WebSocket | ✅ Working | Real-time updates ready |
| Logger | ✅ Working | Enhanced with timestamps |
| Error Handling | ✅ Working | Comprehensive error coverage |
| All Endpoints | ✅ Working | 7 endpoints fully functional |

---

## 📝 Configuration (app/utils/config.py)

```python
@dataclass
class AppConfig:
    enable_stress_test: bool = True      # Run stress tests
    threads: int = 4                     # Concurrent threads
    stress_requests: int = 50            # Load test requests
    report_json: bool = True             # Export JSON
    report_csv: bool = True              # Export CSV
    timeout_seconds: int = 10            # Execution timeout
```

Modify these values to customize behavior.

---

## 🆘 Troubleshooting

### Port already in use
```bash
# Use a different port
uvicorn app.main:app --port 8001
```

### Module not found errors
```bash
# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt
```

### Language compiler not found
- **C++**: Install `g++` → `apt-get install build-essential`
- **Java**: Install `javac` → `apt-get install default-jdk`
- **Node.js**: Install `node` → `apt-get install nodejs`

### Python execution errors
- Verify Python version: `python3 --version` (should be 3.10+)
- Check script syntax before submitting

---

## 📞 Support Resources

- **API Documentation**: Open http://localhost:8000/docs (Swagger UI)
- **API Schema**: http://localhost:8000/openapi.json
- **Logs**: Check console output for detailed error messages
- **Configuration**: Edit `app/utils/config.py` for settings

---

## ✨ Next Steps

1. ✅ **Ready Now**: Start benchmarking code
2. 🔄 **Optional**: Add database for result persistence
3. 🎨 **Optional**: Build frontend dashboard
4. 📊 **Optional**: Integrate Prometheus metrics
5. 🔐 **Optional**: Add authentication/authorization

---

**Happy Benchmarking! 🎯**

*Last updated: 2026-05-12*
