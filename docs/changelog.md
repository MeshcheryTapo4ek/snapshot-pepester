# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.8.0] - 2025-09-20

### Added

- `--max-file-size` flag to skip reading files larger than a specified size (default 2 MiB), preventing large binaries from being processed.

### Changed

- The `exclude_dirs` logic now uses glob pattern matching instead of simple string contains. This allows for more flexible and powerful exclusion rules like `*.egg-info`, `**/__pycache__/**`, etc.
- The default exclusion list has been significantly expanded to include common build artifacts, caches, media files, and logs for cleaner snapshots out-of-the-box.

### Fixed

- Patterns like `*.egg-info` in `exclude_dirs` now work correctly.

## [0.7.0] - 2025-09-19

### Added

- `dir` command: a new mode to scan a single directory without requiring a `rolesnap.yaml` file. It uses sensible default exclusions and saves the output to `rolesnap.json` inside the target directory.

## [0.6.2] - 2025-09-19

### Fixed

- The `rolesnap init` command now correctly finds the template file in installed packages by bundling `rolesnap_example.yaml` as package data and using `importlib.resources` to access it.

### Added

- A comprehensive documentation overhaul, including:
  - A new, more detailed Quickstart guide.
  - A complete `rolesnap.yaml` configuration reference.
  - New pages for Recipes, FAQ, and How-It-Works.
  - An expanded CLI reference with examples for every command.

## [0.6.1] - 2025-09-18

### Changed

- ci! 
  
## [0.5.0] - 2025-09-18

### Added

- Subcommands (`full`, `role`, `selfscan`, `validate`) for a more structured CLI.
- Rich-based colored output and progress bars for better user experience.
- `--quiet` flag to minimize output.
- `--output` flag to specify a custom snapshot file path.
- `--max-bytes` flag to truncate large files.
- `--no-color` flag to disable colored output.
- `validate` subcommand to check the configuration for errors.
- Ruff for linting and formatting.
- `pre-commit` configuration for automated checks.
- Classifiers and keywords to `pyproject.toml` for better package metadata.

### Changed

- **BREAKING**: Removed legacy flags `--role` and `--dir`. Use subcommands instead.
- The project is now named `rolesnap`.
- The main command is now `rolesnap`.
- The configuration file is now `rolesnap.yaml`.
- The output file is now `rolesnap.json`.
- The environment variable is now `ROLESNAP_CONFIG`.
- Examples are moved to the `examples/` directory.
- `DEFAULT_UTILS_DIRS` is now an empty list.

### Removed

- Legacy `snapshoter` entry point.
- `requirements.txt` in favor of `pyproject.toml`
