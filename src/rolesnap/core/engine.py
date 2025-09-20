from __future__ import annotations

import fnmatch
import json
import os
from pathlib import Path

from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from ..logging import console
from .paths import resolve_scan_path, safe_rel_key


def _is_excluded(path: Path, patterns: set[str], root: Path) -> bool:
    """
    Check if a path should be excluded based on glob patterns.

    This function checks multiple things against the patterns without resolving symlinks:
    1. The full relative path (for patterns like 'src/**/*' or '**/__pycache__/**').
    2. Each individual component of the path (for patterns like '*.egg-info' or '.venv').

    Args:
        path: The file or directory path to check.
        patterns: A set of glob patterns to match against.
        root: The root path for resolving the relative path.

    Returns:
        True if the path matches any of the exclusion patterns, False otherwise.
    """
    rel_path_str = safe_rel_key(root, path)
    rel_path_parts = rel_path_str.split("/")

    for pattern in patterns:
        # Check against the full relative path
        if fnmatch.fnmatch(rel_path_str, pattern):
            return True
        # Check against individual path parts
        if any(fnmatch.fnmatch(part, pattern) for part in rel_path_parts):
            return True

    return False


def create_snapshot(
    project_root: Path,
    output_file: Path,
    categories: dict[str, list[str]],
    show_files: bool,
    exclude_dirs: set[str],
    category_roots: dict[str, Path] | None = None,
    quiet: bool = False,
    max_file_size: int | None = None,
) -> None:
    """
    Create a structured snapshot JSON file grouped by categories.

    This is the core function that scans the filesystem, collects files based on
    the provided categories, filters them, reads their content, and writes the
    final JSON output.

    Args:
        project_root: The absolute path to the project's root directory.
        output_file: The path where the final JSON snapshot will be saved.
        categories: A dictionary mapping category names to lists of source paths/globs.
        show_files: If False, file contents will be replaced with "<hidden>".
        exclude_dirs: A set of glob patterns for files/directories to exclude.
        category_roots: A mapping from category names to their specific root paths.
        quiet: If True, suppresses all console output except for errors.
        max_file_size: If set, files larger than this many bytes will be skipped entirely.
    """
    if not categories:
        console.print("No categories provided. Nothing to do.", style="warn")
        return

    all_counts: dict[str, int] = {}
    snapshot: dict[str, dict[str, str]] = {}
    output_file_resolved = output_file.resolve()

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

            resolved_paths: list[Path] = []
            seen_resolved: set[Path] = set()
            for raw in raw_items:
                p = resolve_scan_path(root_for_cat, raw)
                rp = p.resolve()
                if rp in seen_resolved:
                    continue
                seen_resolved.add(rp)
                resolved_paths.append(p)

            if not quiet:
                pretty_sources = ", ".join(safe_rel_key(root_for_cat, p) for p in resolved_paths)
                console.print(f"[category]{cat}[/category] from [path]{pretty_sources}[/path]")

            cat_data: dict[str, str] = {}
            files_to_process: list[Path] = []
            initial_file_count = 0

            for scan_path in resolved_paths:
                if not scan_path.exists():
                    if not quiet:
                        console.print(f"Not found, skipping: {scan_path}", style="warn")
                    continue

                if scan_path.is_dir():
                    # Efficiently walk and prune directories
                    for dirpath, dirnames, filenames in os.walk(scan_path, topdown=True):
                        current_dir = Path(dirpath)
                        # Prune excluded directories
                        dirnames[:] = [
                            d
                            for d in dirnames
                            if not _is_excluded(current_dir / d, exclude_dirs, root_for_cat)
                        ]
                        for filename in filenames:
                            file_path = current_dir / filename
                            if not _is_excluded(file_path, exclude_dirs, root_for_cat):
                                files_to_process.append(file_path)
                elif scan_path.is_file():
                    if not _is_excluded(scan_path, exclude_dirs, root_for_cat):
                        files_to_process.append(scan_path)

            # Filter out the output file itself
            files_to_process = [
                p for p in files_to_process if p.resolve() != output_file_resolved
            ]
            initial_file_count = len(files_to_process)

            task_id = progress.add_task(f"Scanning {cat}", total=initial_file_count)

            for path in files_to_process:
                key = safe_rel_key(root_for_cat, path)
                try:
                    if max_file_size and path.stat().st_size > max_file_size:
                        content = "<skipped_large_file>"
                    elif show_files:
                        content = path.read_text(encoding="utf-8")
                    else:
                        content = "<hidden>"

                    cat_data[key] = content
                except UnicodeDecodeError:
                    pass  # Silently skip non-UTF8 files
                except Exception as e:
                    if not quiet:
                        console.print(f"Error reading file {path}: {e}", style="error")
                finally:
                    progress.advance(task_id)

            # If the original path was a directory and it ended up empty, mark it.
            if not files_to_process and not cat_data:
                for p in resolved_paths:
                    if p.is_dir():
                        dir_key = safe_rel_key(root_for_cat, p)
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
            console.print(
                f"Snapshot created with {total} file(s) across {len(snapshot)} categor(ies).",
                style="success",
            )
            console.print(f"Output file: [path]{output_file}[/path]", style="muted")
    except Exception as e:
        console.print(f"Failed to write snapshot file: {e}", style="error")
