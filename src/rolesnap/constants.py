from __future__ import annotations

# Defaults kept as fallback; real values should come from YAML settings
DEFAULT_EXCLUDE_DIRS: set[str] = {
    ".git",
    ".venv",
    "logs",
    ".env",
    "__pycache__",
    "build",
    "dist",
    ".mypy_cache",
    ".pytest_cache",
}

DEFAULT_UTILS_DIRS: list[str] = []
