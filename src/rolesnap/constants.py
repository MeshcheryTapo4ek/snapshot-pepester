"""
This module defines default constants used throughout the rolesnap application.

These values serve as fallbacks and can be overridden by settings in the
`rolesnap.yaml` configuration file.
"""
from __future__ import annotations

# A set of glob patterns for files and directories to be excluded by default.
# This helps to keep snapshots clean from build artifacts, caches, and irrelevant files.
# The patterns are matched against both the full relative path and individual path segments.
DEFAULT_EXCLUDE_DIRS: set[str] = {
    # Version control
    ".git",
    # Python virtual environments
    ".venv",
    "venv",
    # Build artifacts
    "build",
    "dist",
    "*.egg-info",
    # Caches
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    # IDE and editor directories
    ".idea",
    ".vscode",
    # OS-specific
    ".DS_Store",
    "Thumbs.db",
    # Common log and environment files
    "logs",
    "*.log",
    ".env",
    # Binary and documentation formats that are not useful as source code
    "*.pyc",
    "*.so",
    "*.o",
    "*.dll",
    "*.exe",
    "*.pdf",
    "*.doc",
    "*.docx",
    "*.xls",
    "*.xlsx",
    "*.ppt",
    "*.pptx",
    # Archives
    "*.zip",
    "*.tar",
    "*.gz",
    "*.7z",
    "*.rar",
    # Image files
    "*.png",
    "*.jpg",
    "*.jpeg",
    "*.gif",
    "*.bmp",
    "*.ico",
    "*.tif",
    "*.tiff",
    "*.svg",
    # Audio files
    "*.mp3",
    "*.wav",
    "*.flac",
    # Video files
    "*.mp4",
    "*.mov",
    "*.avi",
    "*.mkv",
}

# Default list of utility directories. This is empty by default and should be
# configured in `rolesnap.yaml` to point to shared code directories.
DEFAULT_UTILS_DIRS: list[str] = []

# Default maximum file size in bytes. Files larger than this will be skipped
# during the snapshot process to avoid including large, non-code assets.
# The default is 2 MiB.
DEFAULT_MAX_FILE_SIZE_BYTES: int = 2 * 1024 * 1024
