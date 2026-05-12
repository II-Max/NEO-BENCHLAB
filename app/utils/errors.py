"""Custom exception classes for NEO BENCHLAB."""

class BenchLabError(Exception):
    """Base exception for NEO BENCHLAB."""
    pass

class UnsupportedLanguageError(BenchLabError):
    """Raised when an unsupported programming language is requested."""
    pass

class CompilationError(BenchLabError):
    """Raised when code compilation fails."""
    pass

class ExecutionError(BenchLabError):
    """Raised when code execution fails."""
    pass

class TimeoutError(BenchLabError):
    """Raised when execution exceeds timeout limit."""
    pass

class SandboxError(BenchLabError):
    """Raised when sandbox operations fail."""
    pass

class ConfigurationError(BenchLabError):
    """Raised when configuration is invalid."""
    pass
