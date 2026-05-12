import asyncio
from dataclasses import dataclass
from typing import Any, Dict
from app.judge.languages import LanguageConfig

@dataclass
class ExecutionResult:
    success: bool
    stdout: str
    stderr: str
    duration: float

class Executor:
    async def execute(self, language_config: LanguageConfig, source: str) -> ExecutionResult:
        cmd = language_config.run_command.format(source=source)
        start = asyncio.get_event_loop().time()
        proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
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
