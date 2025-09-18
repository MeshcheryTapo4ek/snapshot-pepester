from __future__ import annotations

from pathlib import Path
from typing import List, Set

from .paths import safe_rel_key

def compute_self_scan_inputs(project_root: Path, cli_file: Path, config_path: Path) -> List[str]:
    """
    Build a list of paths so that self-scan covers:
      - the CLI file,
      - the rolesnap.core package (resolved dynamically),
      - the YAML config used.
    Prefer relative POSIX keys; skip missing entries; deduplicate results.
    """
    results: List[str] = []
    seen: Set[str] = set()

    def add(path: Path) -> None:
        if not path.exists():
            return
        key = safe_rel_key(project_root, path)
        if key in seen:
            return
        seen.add(key)
        results.append(key)

    # 1) CLI file
    add(cli_file)

    # 2) rolesnap.core package: try import-based resolution first
    pkg_candidate: Path | None = None
    try:
        import rolesnap.core as su
        pkg_candidate = Path(su.__file__).resolve().parent
    except Exception:
        pkg_candidate = None

    if pkg_candidate is not None:
        add(pkg_candidate)

    # Fallback candidates: project root and CLI directory
    add(project_root / "rolesnap" / "core")
    add(cli_file.parent / "core")

    # 3) YAML config
    add(config_path)

    return results
