from __future__ import annotations

from typing import List, Set

# Defaults kept as fallback; real values should come from YAML settings
DEFAULT_EXCLUDE_DIRS: Set[str] = {
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

DEFAULT_UTILS_DIRS: List[str] = []
