from __future__ import annotations

import shutil
from pathlib import Path

from ..logging import console

def resolve_scan_path(root: Path, raw: str) -> Path:
    """
    Resolve a raw path from YAML against the provided project root.
    - Absolute 'raw' -> returned as-is.
    - Relative 'raw' -> merged with 'root' by removing the longest overlap
      between the suffix of 'root.parts' and prefix of 'raw.parts'.
      This avoids duplicated segments like 'trading_agent/trading_agent/...'.
    """
    p = Path(raw).expanduser()
    if p.is_absolute():
        return p.resolve()

    raw_parts = [part for part in p.parts if part not in (".", "")]
    root_parts = list(root.resolve().parts)

    # Find longest l > 0 where raw_parts[:l] == root_parts[-l:]
    max_l = 0
    max_l_candidate = min(len(raw_parts), len(root_parts))
    for l in range(1, max_l_candidate + 1):
        if raw_parts[:l] == root_parts[-l:]:
            max_l = l

    # If overlap exists, drop the overlapping prefix from raw
    tail_parts = raw_parts[max_l:] if max_l > 0 else raw_parts
    merged = Path(*root_parts) / Path(*tail_parts) if tail_parts else Path(*root_parts)
    return merged.resolve()


def safe_rel_key(root: Path, path: Path) -> str:
    """Prefer a key relative to project root, otherwise absolute POSIX."""
    try:
        return path.relative_to(root).as_posix()
    except Exception:
        return path.as_posix()


def remove_pycache(root: Path) -> None:
    """Recursively remove all '__pycache__' directories under the root."""
    console.print(f"🧹 Removing __pycache__ folders in '{root}'...", style="muted")
    count = 0
    for path in root.rglob("__pycache__"):
        if path.is_dir():
            shutil.rmtree(path)
            count += 1
    if count > 0:
        console.print(f"Found and removed {count} __pycache__ folder(s).", style="muted")


def _walk_up(p: Path) -> list[Path]:
    acc: list[Path] = []
    cur = p
    while True:
        acc.append(cur)
        if cur.parent == cur:
            break
        cur = cur.parent
    return acc
