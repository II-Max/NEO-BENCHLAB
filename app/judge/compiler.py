import asyncio
import os
import tempfile
from dataclasses import dataclass
from typing import Any, Dict
from app.judge.languages import LanguageConfig

@dataclass
class CompileResult:
    success: bool
    output: str
    binary_path: str | None = None

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "output": self.output,
            "binary_path": self.binary_path,
        }

class Compiler:
    async def compile_source(self, language_config: LanguageConfig, source: str) -> CompileResult:
        if not language_config.compile_command:
            return CompileResult(success=True, output="skipped", binary_path=None)

        with tempfile.TemporaryDirectory() as tmpdir:
            source_path = os.path.join(tmpdir, language_config.source_name)
            with open(source_path, "w", encoding="utf-8") as handle:
                handle.write(source)

            cmd = language_config.compile_command.format(source=source_path, target=language_config.binary_name)
            proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()
            success = proc.returncode == 0
            return CompileResult(
                success=success,
                output=(stdout.decode() + stderr.decode()).strip(),
                binary_path=os.path.join(tmpdir, language_config.binary_name) if success else None,
            )
