from dataclasses import dataclass
from typing import Dict

@dataclass
class LanguageConfig:
    name: str
    source_name: str
    binary_name: str
    compile_command: str | None
    run_command: str

LANGUAGES: Dict[str, LanguageConfig] = {
    "python": LanguageConfig(
        name="python",
        source_name="submission.py",
        binary_name="",
        compile_command=None,
        run_command="python {source}",
    ),
    "cpp": LanguageConfig(
        name="cpp",
        source_name="submission.cpp",
        binary_name="submission.exe",
        compile_command="g++ {source} -o {target}",
        run_command="{target}",
    ),
    "java": LanguageConfig(
        name="java",
        source_name="Solution.java",
        binary_name="Solution.class",
        compile_command="javac {source}",
        run_command="java -cp . Solution",
    ),
    "nodejs": LanguageConfig(
        name="nodejs",
        source_name="submission.js",
        binary_name="",
        compile_command=None,
        run_command="node {source}",
    ),
}
