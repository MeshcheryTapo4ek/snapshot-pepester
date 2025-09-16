# src/cli.py

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Optional

# Imports are now relative as this module is inside the package
from .engine import create_snapshot
from .paths import remove_pycache
from .planner import collect_role_categories
from .selfscan import compute_self_scan_inputs
from .yaml_loader import load_config_from_yaml, load_roles_from_yaml


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a structured JSON snapshot grouped by categories. Roots per category are supported (project_root, docs_root)."
    )
    add = parser.add_argument
    add("--role", type=str, help="Role name as defined in the YAML config.")
    add("--config", type=str, default="ta_roles.yaml", help="Path to the YAML config file.")
    add("--include-utils", action="store_true", help="Include 'utils' directories from settings into Internal Logic.")
    add("--hide-files", action="store_true", help="Do NOT include file contents (paths only).")
    add("--self-scan", action="store_true", help="Scan only the snapshot tool itself.")
    add("--dir", dest="dirs", action="append", help="Scan only the given directory or file. Repeatable.")
    return parser


def _load_project_root(cfg_path: Path) -> Path:
    cfg = load_config_from_yaml(cfg_path)
    pr = cfg.settings.project_root
    if not pr:
        return Path.cwd().resolve()
    return Path(pr).expanduser().resolve()


def _load_docs_root(cfg_path: Path) -> Optional[Path]:
    cfg = load_config_from_yaml(cfg_path)
    dr = cfg.settings.docs_root
    return Path(dr).expanduser().resolve() if dr else None


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    cfg_path = (
        (Path.cwd() / args.config).resolve()
        if not Path(args.config).is_absolute()
        else Path(args.config)
    )
    cfg = load_config_from_yaml(cfg_path)

    project_root = _load_project_root(cfg_path)
    docs_root = _load_docs_root(cfg_path)
    print(f"Project root: {project_root}")
    if docs_root:
        print(f"Docs root: {docs_root}")
    print(f"Using config: {cfg_path}")

    # --- Измененная логика для определения пути к snapshot.json ---
    if args.dirs:
        first_path = Path(args.dirs[0]).resolve()
        if first_path.is_dir():
            output_snapshot_file = first_path / "snapshot.json"
        else:
            output_snapshot_file = first_path.parent / "snapshot.json"
    else:
        output_snapshot_file = project_root / "snapshot.json"
    # --- Конец измененной логики ---

    # Build categories depending on mode
    if args.dirs:
        print("Mode: DIR")
        categories: Dict[str, List[str]] = {
            "Selected": list(dict.fromkeys(args.dirs))
        }
        category_roots: Dict[str, Path] = {"Selected": project_root}
    elif args.self_scan:
        print("Mode: SELF-SCAN")
        _ = load_roles_from_yaml(cfg_path)  # ensure YAML parses
        categories = {
            "Self-Scan": compute_self_scan_inputs(
                project_root=project_root,
                cli_file=Path(__file__).resolve().parent.parent, # Adjust path to point to package root
                config_path=cfg_path,
            )
        }
        category_roots = {"Self-Scan": project_root}
    elif args.role:
        role_name: str = args.role
        print(f"Mode: ROLE  |  Scan role: {role_name.upper()}")
        categories = collect_role_categories(
            roles=cfg.roles,
            selected_role=role_name,
            include_utils=bool(args.include_utils),
            utils_dirs=cfg.settings.utils_dirs,
        )
        # Map Docs category to docs_root if provided; others to project_root
        category_roots = {k: (docs_root if k == "Docs" and docs_root else project_root) for k in categories}
    else:
        print("Mode: FULL-PROJECT  |  Scan entire repository root with excludes")
        categories = {"Full Project": [project_root.as_posix()]}
        category_roots = {"Full Project": project_root}

    show_files: bool = not bool(args.hide_files)

    remove_pycache(project_root)
    create_snapshot(
        project_root=project_root,
        output_file=output_snapshot_file,
        categories=categories,
        show_files=show_files,
        exclude_dirs=cfg.settings.exclude_dirs,
        category_roots=category_roots,
    )


if __name__ == "__main__":
    main()