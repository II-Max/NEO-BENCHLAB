import asyncio
import tempfile
import os
from dataclasses import dataclass
from typing import Any, Dict
from app.judge.languages import LanguageConfig

@dataclass
class ExecutionResult:
    success: bool
    stdout: str
    stderr: str
    duration: float

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "duration": self.duration,
        }

class Executor:
    async def execute(self, language_config: LanguageConfig, source: str) -> ExecutionResult:
        with tempfile.TemporaryDirectory() as tmpdir:
            source_path = os.path.join(tmpdir, language_config.source_name)
            with open(source_path, "w", encoding="utf-8") as f:
                f.write(source)
            
            cmd = language_config.run_command.format(source=source_path)
            start = asyncio.get_event_loop().time()
            proc = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=tmpdir
            )
            stdout, stderr = await proc.communicate()
            duration = asyncio.get_event_loop().time() - start
            return ExecutionResult(
                success=proc.returncode == 0,
                stdout=stdout.decode(errors="ignore").strip(),
                stderr=stderr.decode(errors="ignore").strip(),
                duration=duration,
            )

    async def execute_source(self, language_config: LanguageConfig, source: str) -> ExecutionResult:
        return await self.execute(language_config, source)
