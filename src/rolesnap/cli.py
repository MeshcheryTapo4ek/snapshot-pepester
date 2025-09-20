from __future__ import annotations

import argparse
import os
import sys
from importlib import resources
from pathlib import Path

from dotenv import load_dotenv

from rolesnap import __version__
from rolesnap.core.engine import create_snapshot
from rolesnap.core.paths import remove_pycache, resolve_config_path
from rolesnap.core.planner import collect_role_categories
from rolesnap.core.selfscan import compute_self_scan_inputs
from rolesnap.constants import DEFAULT_EXCLUDE_DIRS, DEFAULT_MAX_FILE_SIZE_BYTES
from rolesnap.core.yaml_loader import load_config_from_yaml, load_roles_from_yaml
from rolesnap.logging import console

BANNER = r"""
                                                           
,------.        ,--.        ,---.                          
|  .--. ' ,---. |  | ,---. '   .-' ,--,--,  ,--,--. ,---.  
|  '--'.'| .-. ||  || .-. :`.  `-. |      \' ,-.  || .-. | 
|  |\  \ ' '-' '|  |\   --..-'    ||  ||  |\ '-'  || '-' ' 
`--' '--' `---' `--' `----'`-----' `--''--' `--`--'|  |-'  
                                                   `--'    
"""


def _load_project_root(cfg_path: Path) -> Path:
    cfg = load_config_from_yaml(cfg_path)
    pr = cfg.settings.project_root
    return Path(pr).expanduser().resolve() if pr else Path.cwd().resolve()


def _load_docs_root(cfg_path: Path) -> Path | None:
    cfg = load_config_from_yaml(cfg_path)
    dr = cfg.settings.docs_root
    return Path(dr).expanduser().resolve() if dr else None


def _common_after_config(cfg_path: Path) -> tuple[Path, Path | None]:
    project_root = _load_project_root(cfg_path)
    docs_root = _load_docs_root(cfg_path)
    console.print(f"Project root: [path]{project_root}[/path]", style="muted")
    if docs_root:
        console.print(f"Docs root:    [path]{docs_root}[/path]", style="muted")
    console.print(f"Using config: [path]{cfg_path}[/path]", style="muted")
    return project_root, docs_root


def _cmd_dir(
    path_str: str,
    show_files: bool,
    output: Path | None,
    quiet: bool,
    max_file_size: int,
) -> None:
    """Execute the 'dir' command to scan a single directory."""
    scan_path = Path(path_str).expanduser().resolve()
    if not scan_path.is_dir():
        console.print(f"Error: Path is not a directory: {scan_path}", style="error")
        raise SystemExit(1)

    console.print(f"Scanning directory: [path]{scan_path}[/path]", style="info")
    remove_pycache(scan_path, quiet=quiet)
    categories: dict[str, list[str]] = {"Scanned Directory": [scan_path.as_posix()]}
    output_file = output or scan_path / "rolesnap.json"

    create_snapshot(
        project_root=scan_path,
        output_file=output_file,
        categories=categories,
        show_files=show_files,
        exclude_dirs=DEFAULT_EXCLUDE_DIRS,
        category_roots={"Scanned Directory": scan_path},
        quiet=quiet,
        max_file_size=max_file_size,
    )


def _cmd_full(
    cfg_path: Path,
    show_files: bool,
    output: Path | None,
    quiet: bool,
    max_file_size: int,
) -> None:
    """Execute the 'full' command to scan the entire project."""
    project_root, _ = _common_after_config(cfg_path)
    remove_pycache(project_root, quiet=quiet)
    categories: dict[str, list[str]] = {"Full Project": [project_root.as_posix()]}
    create_snapshot(
        project_root=project_root,
        output_file=output or project_root / "rolesnap.json",
        categories=categories,
        show_files=show_files,
        exclude_dirs=load_config_from_yaml(cfg_path).settings.exclude_dirs,
        category_roots={"Full Project": project_root},
        quiet=quiet,
        max_file_size=max_file_size,
    )


def _cmd_role(
    cfg_path: Path,
    role_name: str,
    include_utils: bool,
    show_files: bool,
    output: Path | None,
    quiet: bool,
    max_file_size: int,
) -> None:
    """Execute the 'role' command to scan a specific role."""
    project_root, docs_root = _common_after_config(cfg_path)
    cfg = load_config_from_yaml(cfg_path)
    remove_pycache(project_root, quiet=quiet)
    categories = collect_role_categories(
        roles=cfg.roles,
        selected_role=role_name,
        include_utils=include_utils,
        utils_dirs=cfg.settings.utils_dirs,
    )
    category_roots = {
        k: (docs_root if k == "Docs" and docs_root else project_root) for k in categories
    }
    create_snapshot(
        project_root=project_root,
        output_file=output or project_root / "rolesnap.json",
        categories=categories,
        show_files=show_files,
        exclude_dirs=cfg.settings.exclude_dirs,
        category_roots=category_roots,
        quiet=quiet,
        max_file_size=max_file_size,
    )


def _cmd_selfscan(
    cfg_path: Path,
    show_files: bool,
    output: Path | None,
    quiet: bool,
    max_file_size: int,
) -> None:
    """Execute the 'selfscan' command to scan the tool's own source code."""
    project_root, _ = _common_after_config(cfg_path)
    _ = load_roles_from_yaml(cfg_path)
    remove_pycache(project_root, quiet=quiet)
    categories = {
        "Self-Scan": compute_self_scan_inputs(
            project_root=project_root,
            cli_dir=Path(__file__).resolve().parent.parent,
            config_path=cfg_path,
        )
    }
    create_snapshot(
        project_root=project_root,
        output_file=output or project_root / "rolesnap.json",
        categories=categories,
        show_files=show_files,
        exclude_dirs=load_config_from_yaml(cfg_path).settings.exclude_dirs,
        category_roots={"Self-Scan": project_root},
        quiet=quiet,
        max_file_size=max_file_size,
    )


def _cmd_validate(cfg_path: Path) -> None:
    """Execute the 'validate' command to check the configuration file."""
    cfg = load_config_from_yaml(cfg_path)
    missing = []
    pr = Path(cfg.settings.project_root or Path.cwd()).resolve()

    def _check(paths: list[str]):
        for raw in paths:
            p = Path(raw)
            if not p.is_absolute():
                p = (pr / raw).resolve()
            if not p.exists():
                missing.append(raw)

    for _, role in cfg.roles.items():
        _check(
            role.external_ports
            + role.external_domain
            + role.internal_logic
            + role.base_tasks
            + role.advanced_tasks
            + role.docs
        )
    if missing:
        console.print("Config valid, but missing paths:", style="warn")
        for m in sorted(set(missing)):
            console.print(f" - {m}", style="path")
        raise SystemExit(2)
    console.print(f"Config OK. Roles: {', '.join(sorted(cfg.roles.keys()))}", style="success")


def _cmd_init() -> None:
    """Execute the 'init' command to create a default configuration file."""
    console.print("Initializing rolesnap configuration...", style="info")
    roles_dir = Path.cwd() / "docs" / "roles"
    roles_dir.mkdir(parents=True, exist_ok=True)
    config_path = roles_dir / "rolesnap.yaml"
    if config_path.exists():
        console.print(
            f"Configuration file already exists at [path]{config_path}[/path]", style="warn"
        )
        return

    example_path: Path | None = None
    try:
        # rolesnap/examples/rolesnap_example.yaml inside package
        with resources.as_file(resources.files("rolesnap").joinpath("examples/rolesnap_example.yaml")) as p:
            example_path = p
    except Exception:
        example_path = None

    if example_path is None or not example_path.exists():
        # last resort: repo layout for dev installs
        candidate = Path(__file__).parent / "examples" / "rolesnap_example.yaml"
        example_path = candidate if candidate.exists() else None

    if example_path is None:
        console.print("Could not find example configuration inside the package.", style="error")
        raise SystemExit(1)

    content = example_path.read_text()
    # Replace the placeholder project_root with the current working directory
    content = content.replace("/path/to/your/project", str(Path.cwd()))

    # Also replace docs_root if a 'docs' directory exists in the current directory
    docs_dir = Path.cwd() / "docs"
    if docs_dir.is_dir():
        content = content.replace("/path/to/your/docs", str(docs_dir.resolve()))

    config_path.write_text(content)
    console.print(f"Created configuration file at [path]{config_path}[/path]", style="success")
    console.print(
        "Please review the file and adjust the paths to your project structure.", style="info"
    )


def build_arg_parser() -> argparse.ArgumentParser:
    """
    Build the argument parser for the CLI.

    This function defines all commands, subcommands, and flags that the user
    can interact with.

    Returns:
        The configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        description="Create a structured JSON snapshot grouped by categories."
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to rolesnap.yaml. If not set, uses ROLESNAP_CONFIG from .env/env.",
    )
    parser.add_argument(
        "--hide-files", action="store_true", help="Do NOT include file contents (paths only)."
    )
    parser.add_argument("--no-banner", action="store_true", help="Do not display the banner.")
    parser.add_argument("--version", action="store_true", help="Display the version and exit.")
    parser.add_argument(
        "--quiet", action="store_true", help="Minimal output, no banner or progress."
    )
    parser.add_argument("--output", type=Path, default=None, help="Path to write the snapshot to.")
    parser.add_argument(
        "--max-file-size",
        type=int,
        default=DEFAULT_MAX_FILE_SIZE_BYTES,
        help=f"Skip files larger than N bytes. Default: {DEFAULT_MAX_FILE_SIZE_BYTES} (2 MiB).",
    )
    parser.add_argument("--no-color", action="store_true", help="Disable color output.")

    subs = parser.add_subparsers(dest="cmd")

    p_dir = subs.add_parser("dir", help="Scan a single directory with default excludes.")
    p_dir.add_argument("path", type=str, help="Path to the directory to scan.")

    subs.add_parser("full", help="Scan entire project_root with excludes.")

    p_role = subs.add_parser("role", help="Scan a single role defined in rolesnap.yaml.")
    p_role.add_argument("name", type=str, help="Role name to scan.")
    p_role.add_argument(
        "--include-utils", action="store_true", help="Include 'utils' dirs into Internal Logic."
    )

    subs.add_parser("selfscan", help="Scan the rolesnap tool itself.")

    subs.add_parser("validate", help="Validate rolesnap.yaml and paths.")

    subs.add_parser("init", help="Create a default rolesnap.yaml in docs/roles.")

    return parser


def main() -> None:
    """The main entry point for the rolesnap CLI."""
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.no_color or not os.sys.stdout.isatty():
        from rolesnap.logging import reinit_console

        reinit_console(color_system=None)

    if args.quiet:
        console.quiet = True

    if args.version:
        console.print(f"rolesnap version {__version__}", style="info")
        raise SystemExit(0)

    if args.cmd == "init":
        _cmd_init()
        return

    if not args.no_banner and not args.quiet:
        console.print(BANNER, style="muted")

    show_files: bool = not bool(args.hide_files)
    quiet: bool = args.quiet

    if args.cmd == "dir":
        _cmd_dir(args.path, show_files, args.output, quiet, args.max_file_size)
        return

    load_dotenv(override=False)
    cwd = Path.cwd().resolve()
    cfg_path = resolve_config_path(cwd=cwd, cli_config=args.config)

    if args.cmd == "validate":
        _cmd_validate(cfg_path)
        return

    if args.cmd == "full":
        _cmd_full(cfg_path, show_files, args.output, quiet, args.max_file_size)
        return
    if args.cmd == "role":
        _cmd_role(
            cfg_path,
            args.name,
            args.include_utils,
            show_files,
            args.output,
            quiet,
            args.max_file_size,
        )
        return
    if args.cmd == "selfscan":
        _cmd_selfscan(cfg_path, show_files, args.output, quiet, args.max_file_size)
        return

    # default: full
    _cmd_full(cfg_path, show_files, args.output, quiet, args.max_file_size)


if __name__ == "__main__":
    main()
