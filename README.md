# NEO BENCHLAB

Professional Benchmark & Performance Analysis Platform for Online Judge Systems.

## Overview

NEO BENCHLAB is designed to benchmark source code execution, monitor system resources, run stress tests, and generate detailed reports for online judge workflows.

## Structure

- `app/main.py`: FastAPI entrypoint
- `app/benchmark/`: benchmark engine, reporting, profiling, and monitoring
- `app/judge/`: compilation, execution, sandboxing, and queue management
- `app/dashboard/`: realtime dashboard endpoints and WebSocket support
- `app/utils/`: shared configuration, logging, timing, and helpers

## Install

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

## Endpoints

- `GET /stats`
- `GET /benchmarks`
- `POST /benchmark/run`
- `GET /reports`
- `GET /system/health`

## Notes

This repository contains an initial scaffold for the NEO BENCHLAB platform. The current implementation includes placeholder modules and stub endpoints for further development.
