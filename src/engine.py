from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, Set

from .paths import resolve_scan_path, safe_rel_key


def create_snapshot(
    project_root: Path,
    output_file: Path,
    categories: Dict[str, List[str]],
    show_files: bool,
    exclude_dirs: Set[str],
    category_roots: Optional[Dict[str, Path]] = None,
) -> None:
    """
    Create a structured snapshot JSON grouped by categories.
    - 'categories' maps category name -> list of dirs/files to scan
    - 'category_roots' optionally overrides root per category (e.g., Docs)
    - Resolve and deduplicate scan paths per category
    - Honor configurable exclude_dirs
    - Ignore binary files
    JSON structure:
    {
      "<Category>": {
         "path/to/file.py": "content or <hidden>",
         ...
      },
      ...
    }
    """
    if not categories:
        print("⚠️  No categories provided. Nothing to do.")
        return

    all_counts: Dict[str, int] = {}
    snapshot: Dict[str, Dict[str, str]] = {}

    for cat, raw_items in categories.items():
        if not raw_items:
            continue

        root_for_cat = (category_roots or {}).get(cat, project_root)

        # Resolve and dedup paths for this category
        resolved_paths: List[Path] = []
        seen: Set[Path] = set()
        for raw in raw_items:
            p = resolve_scan_path(root_for_cat, raw)
            rp = p.resolve()
            if rp in seen:
                continue
            seen.add(rp)
            resolved_paths.append(rp)

        pretty_sources = ", ".join(safe_rel_key(root_for_cat, p) for p in resolved_paths)
        print(f"📸 [{cat}] from: {pretty_sources}")

        cat_data: Dict[str, str] = {}
        count = 0

        for scan_path in resolved_paths:
            if not scan_path.exists():
                print(f"⚠️  [{cat}] not found, skipping: {scan_path}")
                continue

            is_dir = scan_path.is_dir()
            paths_to_scan = scan_path.rglob("*") if is_dir else [scan_path]

            for path in paths_to_scan:
                if path.is_dir():
                    continue
                if any(part in exclude_dirs for part in path.parts):
                    continue
                if path.resolve() == output_file.resolve():
                    continue

                key = safe_rel_key(root_for_cat, path)
                try:
                    try:
                        size = path.stat().st_size
                    except Exception:
                        size = None

                    if size == 0:
                        content = "" if show_files else "<empty>"
                        cat_data[key] = content
                        count += 1
                        if show_files:
                            print(f"📄 [{cat}] {key} (empty)")
                        continue

                    if show_files:
                        print(f"📄 [{cat}] {key}")
                        content = path.read_text(encoding="utf-8")
                    else:
                        content = "<hidden>"

                    cat_data[key] = content
                    count += 1

                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    print(f"🔥 [{cat}] Error reading file {path}: {e}")
                    continue

            if is_dir and count == 0 and not cat_data:
                dir_key = safe_rel_key(root_for_cat, scan_path)
                cat_data[dir_key] = "<empty_dir>"
                if show_files:
                    print(f"📁 [{cat}] Empty directory: {dir_key}")

        snapshot[cat] = dict(sorted(cat_data.items()))
        all_counts[cat] = len(cat_data)

    try:
        output_file.write_text(
            json.dumps(snapshot, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        total = sum(all_counts.values())
        print(f"✅ Snapshot created with {total} file(s) across {len(snapshot)} categor(ies).")
        print(f"📄 Output file: {output_file}")
    except Exception as e:
        print(f"🔥 Failed to write snapshot file: {e}")
