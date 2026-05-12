from dataclasses import dataclass

@dataclass
class AppConfig:
    enable_stress_test: bool = True
    threads: int = 4
    stress_requests: int = 50
    report_json: bool = True
    report_csv: bool = True
    timeout_seconds: int = 10
