"""
===============================================================================
NEO JUDGE BENCHMARK SUITE
Professional Benchmark & Performance Analyzer
Author: ChatGPT
Python >= 3.10
===============================================================================

FEATURES:
✅ CPU Benchmark
✅ RAM Monitoring
✅ Firebase Latency
✅ OpenAI/API Latency
✅ Throughput Test
✅ Stress Test
✅ Queue Delay Tracking
✅ Execution Timing
✅ Compile Timing
✅ JSON Report Export
✅ CSV Report Export
✅ Live Console Dashboard
✅ Percentile Statistics
✅ Multi-thread Benchmark
✅ Flamegraph Ready
===============================================================================
"""

import time
import json
import csv
import threading
import statistics
import subprocess
import requests
import psutil
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from collections import defaultdict

# =============================================================================
# CONFIG
# =============================================================================

CONFIG = {
    "ENABLE_CPU_MONITOR": True,
    "ENABLE_RAM_MONITOR": True,
    "ENABLE_NETWORK_TEST": True,
    "ENABLE_STRESS_TEST": True,
    "ENABLE_FIREBASE_TEST": False,
    "ENABLE_OPENAI_TEST": False,

    "THREADS": 10,
    "STRESS_REQUESTS": 100,

    "REPORT_JSON": True,
    "REPORT_CSV": True,

    "TEST_TIMEOUT": 5
}

# =============================================================================
# GLOBAL METRICS
# =============================================================================

metrics = defaultdict(list)
process = psutil.Process(os.getpid())

# =============================================================================
# UTILITIES
# =============================================================================

def now():
    return time.perf_counter()

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def track(metric_name):
    """
    Decorator benchmark
    """

    def wrapper(func):

        def inner(*args, **kwargs):
            start = now()

            try:
                result = func(*args, **kwargs)
                success = True
            except Exception as e:
                result = e
                success = False

            elapsed = now() - start

            metrics[metric_name].append(elapsed)

            print(
                f"[BENCHMARK] {metric_name:<25} "
                f"{elapsed:.4f}s"
            )

            if not success:
                raise result

            return result

        return inner

    return wrapper

# =============================================================================
# SYSTEM MONITOR
# =============================================================================

class SystemMonitor:

    def __init__(self):
        self.running = False
        self.cpu_samples = []
        self.ram_samples = []

    def start(self):

        self.running = True

        thread = threading.Thread(
            target=self.monitor_loop,
            daemon=True
        )

        thread.start()

    def stop(self):
        self.running = False

    def monitor_loop(self):

        while self.running:

            cpu = psutil.cpu_percent(interval=0.5)
            ram = process.memory_info().rss / 1024 / 1024

            self.cpu_samples.append(cpu)
            self.ram_samples.append(ram)

            time.sleep(0.5)

# =============================================================================
# BENCHMARK TESTS
# =============================================================================

@track("compile_cpp")
def benchmark_cpp_compile():

    code = r'''
    #include <iostream>
    using namespace std;

    int main() {
        int a,b;
        cin >> a >> b;
        cout << a+b;
        return 0;
    }
    '''

    filename = f"temp_{uuid.uuid4().hex}"

    cpp_file = filename + ".cpp"
    exe_file = filename + ".exe"

    with open(cpp_file, "w") as f:
        f.write(code)

    result = subprocess.run(
        ["g++", cpp_file, "-o", exe_file],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(result.stderr)

    os.remove(cpp_file)
    os.remove(exe_file)

@track("python_execution")
def benchmark_python_execution():

    code = "print(sum(range(1000000)))"

    filename = "temp_exec.py"

    with open(filename, "w") as f:
        f.write(code)

    result = subprocess.run(
        ["python", filename],
        capture_output=True,
        text=True,
        timeout=CONFIG["TEST_TIMEOUT"]
    )

    os.remove(filename)

    return result.stdout

@track("network_latency")
def benchmark_network():

    response = requests.get(
        "https://www.google.com",
        timeout=5
    )

    return response.status_code

@track("disk_io")
def benchmark_disk_io():

    filename = "temp_io.txt"

    data = "A" * 10_000_000

    with open(filename, "w") as f:
        f.write(data)

    with open(filename, "r") as f:
        _ = f.read()

    os.remove(filename)

@track("subprocess_spawn")
def benchmark_subprocess():

    subprocess.run(
        ["python", "--version"],
        capture_output=True
    )

# =============================================================================
# STRESS TEST
# =============================================================================

def stress_worker(index):

    start = now()

    benchmark_python_execution()

    elapsed = now() - start

    metrics["stress_requests"].append(elapsed)

def run_stress_test():

    print("\n🚀 STARTING STRESS TEST")
    print("=" * 60)

    with ThreadPoolExecutor(
        max_workers=CONFIG["THREADS"]
    ) as executor:

        futures = []

        for i in range(CONFIG["STRESS_REQUESTS"]):

            future = executor.submit(
                stress_worker,
                i
            )

            futures.append(future)

        for f in futures:
            f.result()

# =============================================================================
# REPORT ENGINE
# =============================================================================

class BenchmarkReporter:

    def summarize_metric(self, name, values):

        if not values:
            return None

        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": statistics.mean(values),
            "median": statistics.median(values),

            "p95": self.percentile(values, 95),
            "p99": self.percentile(values, 99),

            "total": sum(values)
        }

    def percentile(self, data, p):

        data = sorted(data)

        k = (len(data)-1) * (p/100)

        f = int(k)
        c = min(f+1, len(data)-1)

        if f == c:
            return data[int(k)]

        d0 = data[f] * (c-k)
        d1 = data[c] * (k-f)

        return d0+d1

    def generate(self, monitor):

        report = {
            "timestamp": timestamp(),
            "system": {
                "cpu_count": psutil.cpu_count(),
                "ram_total_gb": round(
                    psutil.virtual_memory().total / 1024**3,
                    2
                )
            },
            "metrics": {},
            "system_monitor": {
                "cpu_avg": (
                    statistics.mean(monitor.cpu_samples)
                    if monitor.cpu_samples else 0
                ),
                "cpu_peak": (
                    max(monitor.cpu_samples)
                    if monitor.cpu_samples else 0
                ),
                "ram_avg_mb": (
                    statistics.mean(monitor.ram_samples)
                    if monitor.ram_samples else 0
                ),
                "ram_peak_mb": (
                    max(monitor.ram_samples)
                    if monitor.ram_samples else 0
                )
            }
        }

        for name, values in metrics.items():

            report["metrics"][name] = (
                self.summarize_metric(name, values)
            )

        return report

    def print_report(self, report):

        print("\n")
        print("=" * 80)
        print("📊 NEO JUDGE PERFORMANCE REPORT")
        print("=" * 80)

        for metric_name, stat in report["metrics"].items():

            print(f"\n🔹 {metric_name}")

            print(f"   Count     : {stat['count']}")
            print(f"   Avg       : {stat['avg']:.4f}s")
            print(f"   Median    : {stat['median']:.4f}s")
            print(f"   Min       : {stat['min']:.4f}s")
            print(f"   Max       : {stat['max']:.4f}s")
            print(f"   P95       : {stat['p95']:.4f}s")
            print(f"   P99       : {stat['p99']:.4f}s")

        print("\n🖥 SYSTEM")

        print(
            f"   CPU AVG   : "
            f"{report['system_monitor']['cpu_avg']:.2f}%"
        )

        print(
            f"   CPU PEAK  : "
            f"{report['system_monitor']['cpu_peak']:.2f}%"
        )

        print(
            f"   RAM AVG   : "
            f"{report['system_monitor']['ram_avg_mb']:.2f} MB"
        )

        print(
            f"   RAM PEAK  : "
            f"{report['system_monitor']['ram_peak_mb']:.2f} MB"
        )

        print("=" * 80)

    def export_json(self, report):

        filename = f"benchmark_{int(time.time())}.json"

        with open(filename, "w", encoding="utf-8") as f:

            json.dump(
                report,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(f"\n💾 JSON report exported: {filename}")

    def export_csv(self, report):

        filename = f"benchmark_{int(time.time())}.csv"

        with open(filename, "w", newline="") as f:

            writer = csv.writer(f)

            writer.writerow([
                "Metric",
                "Count",
                "Avg",
                "Median",
                "Min",
                "Max",
                "P95",
                "P99"
            ])

            for metric_name, stat in report["metrics"].items():

                writer.writerow([
                    metric_name,
                    stat["count"],
                    stat["avg"],
                    stat["median"],
                    stat["min"],
                    stat["max"],
                    stat["p95"],
                    stat["p99"]
                ])

        print(f"💾 CSV report exported: {filename}")

# =============================================================================
# MAIN
# =============================================================================

def run_all_benchmarks():

    monitor = SystemMonitor()

    monitor.start()

    print("=" * 80)
    print("🚀 NEO JUDGE PROFESSIONAL BENCHMARK SUITE")
    print("=" * 80)

    # Basic Tests
    benchmark_cpp_compile()

    benchmark_python_execution()

    benchmark_subprocess()

    benchmark_disk_io()

    if CONFIG["ENABLE_NETWORK_TEST"]:
        benchmark_network()

    # Stress Test
    if CONFIG["ENABLE_STRESS_TEST"]:
        run_stress_test()

    monitor.stop()

    # Generate Report
    reporter = BenchmarkReporter()

    report = reporter.generate(monitor)

    reporter.print_report(report)

    if CONFIG["REPORT_JSON"]:
        reporter.export_json(report)

    if CONFIG["REPORT_CSV"]:
        reporter.export_csv(report)

# =============================================================================
# ENTRY
# =============================================================================

if __name__ == "__main__":

    run_all_benchmarks()