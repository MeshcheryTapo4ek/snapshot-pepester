# Gemini Agent Instructions for `rolesnap`

## Project Overview

`rolesnap` is a Python CLI tool designed to create role-based, structured snapshots of a codebase. It is particularly useful for generating context for Large Language Models (LLMs) and for enforcing architectural boundaries.

The main technologies used are:
- **Python 3.11+**
- **`rich`**: For colored terminal output and progress bars.
- **`pyyaml`**: For parsing the YAML configuration.
- **`python-dotenv`**: For loading environment variables from a `.env` file.

The project follows a modular architecture with a core engine that handles the snapshot creation and a CLI layer that parses arguments and calls the engine.

## Building and Running

### Installation

The project uses `uv` for dependency management. To install the project in editable mode, run:

```bash
uv pip install -e .
```

This will install the `rolesnap` command in the virtual environment.

### Running

The tool is run from the command line using the `rolesnap` command. It has several subcommands:

- `rolesnap full`: Scan the entire project root.
- `rolesnap role <name>`: Scan a single role defined in `rolesnap.yaml`.
- `rolesnap selfscan`: Scan the `rolesnap` tool itself.
- `rolesnap validate`: Validate the configuration file.

### Configuration

The tool is configured via a `rolesnap.yaml` file. The path to this file can be specified using the `--config` flag or the `ROLESNAP_CONFIG` environment variable. An example configuration file is available at `examples/rolesnap_example.yaml`.

### Testing

The project uses `pytest` for testing. To run the tests, first install the development dependencies:

```bash
uv pip install -e .[dev]
```

Then run `pytest`:

```bash
pytest
```

## Development Conventions

### Code Style

The project uses `ruff` for linting and formatting. The configuration is in `pyproject.toml`. It is recommended to use the `pre-commit` hooks to automatically format the code before committing:

```bash
pre-commit install
```

### Contribution Guidelines

- All new features should be accompanied by tests.
- Code should be formatted with `ruff`.
- The `CHANGELOG.md` should be updated for any user-facing changes.
