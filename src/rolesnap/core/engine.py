from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, Set

from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from ..logging import console
from .paths import resolve_scan_path, safe_rel_key

BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".tif", ".tiff",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".zip", ".tar", ".gz", ".7z", ".rar",
    ".exe", ".dll", ".so", ".a", ".lib", ".o", ".obj",
    ".pyc", ".pyd",
    ".ipynb",
}

def create_snapshot(
    project_root: Path,
    output_file: Path,
    categories: Dict[str, List[str]],
    show_files: bool,
    exclude_dirs: Set[str],
    category_roots: Optional[Dict[str, Path]] = None,
    max_bytes: Optional[int] = None,
    quiet: bool = False,
) -> None:
    """
    Create a structured snapshot JSON grouped by categories.
    """
    if not categories:
        console.print("No categories provided. Nothing to do.", style="warn")
        return

    all_counts: Dict[str, int] = {}
    snapshot: Dict[str, Dict[str, str]] = {}

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
        transient=False,
        disable=quiet,
    ) as progress:
        for cat, raw_items in categories.items():
            if not raw_items:
                continue

            root_for_cat = (category_roots or {}).get(cat, project_root)

            resolved_paths: List[Path] = []
            seen: Set[Path] = set()
            for raw in raw_items:
                p = resolve_scan_path(root_for_cat, raw)
                rp = p.resolve()
                if rp in seen:
                    continue
                seen.add(rp)
                resolved_paths.append(rp)

            if not quiet:
                pretty_sources = ", ".join(safe_rel_key(root_for_cat, p) for p in resolved_paths)
                console.print(f"[category]{cat}[/category] from [path]{pretty_sources}[/path]")

            cat_data: Dict[str, str] = {}
            files_list: List[Path] = []

            for scan_path in resolved_paths:
                if not scan_path.exists():
                    if not quiet:
                        console.print(f"Not found, skipping: {scan_path}", style="warn")
                    continue
                if scan_path.is_dir():
                    files_list.extend([p for p in scan_path.rglob("*") if p.is_file()])
                else:
                    files_list.append(scan_path)

            files_list = [
                p for p in files_list
                if not any(part in exclude_dirs for part in p.parts)
                and p.resolve() != output_file.resolve()
                and p.suffix not in BINARY_EXTENSIONS
            ]

            task_id = progress.add_task(f"Scanning {cat}", total=len(files_list))

            for path in files_list:
                key = safe_rel_key(root_for_cat, path)
                try:
                    if show_files:
                        content = path.read_text(encoding="utf-8")
                        if max_bytes and len(content) > max_bytes:
                            content = content[:max_bytes]
                    else:
                        content = "<hidden>"

                    cat_data[key] = content
                except UnicodeDecodeError:
                    pass
                except Exception as e:
                    if not quiet:
                        console.print(f"Error reading file {path}: {e}", style="error")
                finally:
                    progress.advance(task_id)

            if not files_list and not cat_data and not quiet:
                dir_key = safe_rel_key(root_for_cat, resolved_paths[0])
                cat_data[dir_key] = "<empty_dir>"

            snapshot[cat] = dict(sorted(cat_data.items()))
            all_counts[cat] = len(cat_data)

    try:
        output_file.write_text(
            json.dumps(snapshot, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        if not quiet:
            total = sum(all_counts.values())
            console.print(f"Snapshot created with {total} file(s) across {len(snapshot)} categor(ies).", style="success")
            console.print(f"Output file: [path]{output_file}[/path]", style="muted")
    except Exception as e:
        console.print(f"Failed to write snapshot file: {e}", style="error")
