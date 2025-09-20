"""
This module contains utility functions for path manipulation and resolution.

It handles resolving YAML paths against a project root, creating safe relative
path keys for the snapshot, and finding the configuration file.
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path

from ..logging import console


def resolve_scan_path(root: Path, raw: str) -> Path:
    """
    Resolve a raw path from YAML against the provided project root.

    This function intelligently merges a root path and a raw path string.
    - If 'raw' is absolute, it's returned as-is.
    - If 'raw' is relative, it removes the longest overlapping segment between
      the end of the `root` path and the start of the `raw` path.
      This avoids duplicated path segments (e.g., `src/api` + `src/api/main.py`).

    Args:
        root: The absolute root path to resolve against.
        raw: The raw path string from the configuration (can be relative or absolute).

    Returns:
        The resolved absolute path.
    """
    p = Path(raw).expanduser()
    if p.is_absolute():
        return p.resolve()

    raw_parts = [part for part in p.parts if part not in (".", "")]
    root_parts = list(root.resolve().parts)

    # Find longest l > 0 where raw_parts[:l] == root_parts[-l:]
    max_l = 0
    max_l_candidate = min(len(raw_parts), len(root_parts))
    for line_count in range(1, max_l_candidate + 1):
        if raw_parts[:line_count] == root_parts[-line_count:]:
            max_l = line_count

    # If overlap exists, drop the overlapping prefix from raw
    tail_parts = raw_parts[max_l:] if max_l > 0 else raw_parts
    merged = Path(*root_parts) / Path(*tail_parts) if tail_parts else Path(*root_parts)
    return merged.resolve()


def safe_rel_key(root: Path, path: Path) -> str:
    """
    Create a safe, POSIX-style relative path key for a given path.

    It attempts to make `path` relative to `root`. If that fails (e.g., they are
    on different drives), it falls back to the absolute POSIX path of `path`.

    Args:
        root: The root directory to make the path relative to.
        path: The path to convert into a key.

    Returns:
        A string representing the relative path, or the absolute path as a fallback.
    """
    try:
        return path.relative_to(root).as_posix()
    except Exception:
        return path.as_posix()


def remove_pycache(root: Path, quiet: bool = False) -> None:
    """
    Recursively find and remove all '__pycache__' directories under a given root.

    Args:
        root: The directory where the search for `__pycache__` folders will start.
        quiet: If True, suppresses all console output.
    """
    if not quiet:
        console.print(f"🧹 Removing __pycache__ folders in '{root}'...", style="muted")
    count = 0
    for path in root.rglob("__pycache__"):
        if path.is_dir():
            shutil.rmtree(path)
            count += 1
    if count > 0 and not quiet:
        console.print(f"Found and removed {count} __pycache__ folder(s).", style="muted")


def resolve_config_path(cwd: Path, cli_config: str | None) -> Path:
    """
    Find the `rolesnap.yaml` configuration file and return its absolute path.

    The search order is:
    1. The path provided by the `--config` CLI argument.
    2. The path specified in the `ROLESNAP_CONFIG` environment variable.

    If a path is relative, it is resolved against the current working directory.
    The program will exit if the file is not found.

    Args:
        cwd: The current working directory, used to resolve relative paths.
        cli_config: The value from the `--config` CLI flag, if provided.

    Returns:
        The absolute path to the found configuration file.

    Raises:
        SystemExit: If no config file can be found.
    """
    if cli_config:
        p = Path(cli_config).expanduser()
        if not p.is_absolute():
            p = (cwd / p).resolve()
        if not p.is_file():
            console.print(f"--config file not found: {p}", style="error")
            raise SystemExit(2)
        console.print(f"Using config from --config: [path]{p}[/path]", style="info")
        return p

    env_val = os.getenv("ROLESNAP_CONFIG")
    if not env_val:
        console.print("ROLESNAP_CONFIG is not set and --config is not provided.", style="error")
        console.print(
            "Hint: add 'ROLESNAP_CONFIG=./rolesnap.yaml' to your .env or pass --config /abs/path/to/rolesnap.yaml",
            style="muted",
        )
        raise SystemExit(2)

    p = Path(env_val).expanduser()
    if not p.is_absolute():
        p = (cwd / p).resolve()
    if not p.is_file():
        console.print(f"ROLESNAP_CONFIG points to non-existing file: {p}", style="error")
        raise SystemExit(2)

    console.print(f"Using config from ENV ROLESNAP_CONFIG: [path]{p}[/path]", style="info")
    return p
