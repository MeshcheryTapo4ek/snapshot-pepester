# Rolesnap

[![PyPI](https://img.shields.io/pypi/v/rolesnap.svg)](https://pypi.org/project/rolesnap/)
![Python](https://img.shields.io/pypi/pyversions/rolesnap.svg)
[![CI](https://github.com/MeshcheryTapo4ek/snapshot-pepester/actions/workflows/ci.yml/badge.svg)](https://github.com/MeshcheryTapo4ek/snapshot-pepester/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-mkdocs--material-success)](https://meshcherytapo4ek.github.io/snapshot-pepester/)
[![Code style](https://img.shields.io/badge/ruff-mypy-informational)](#)

A CLI tool for creating role-based, structured snapshots of your codebase, perfect for generating LLM context and enforcing architectural boundaries.

## Quickstart

```bash
pipx install rolesnap          # option 1: global and isolated
# or
uv tool install rolesnap       # option 2: as a tool via uv

rolesnap --version
```

### Install options
```bash
# Into a project:
uv add rolesnap
uv run rolesnap full --config rolesnap.yaml
```

---

## Why Rolesnap?

*   **Precision Context for LLMs**: Stop feeding excess code to your AI. Generate focused snapshots containing only the files relevant to a specific feature, service, or architectural layer.
*   **Declarative Architecture**: Define your project's components as "Roles" in a simple YAML file. This configuration becomes a living, executable document of your system's architecture.
*   **Enforce Architectural Boundaries**: By explicitly defining the public API of each module, the tool helps you visualize and maintain a clean, modular, or hexagonal architecture.

> [!TIP]
> For a deep dive, check out the full documentation at **https://meshcherytapo4ek.github.io/snapshot-pepester/**

---

## What Is This?

**Rolesnap** is a command-line utility designed to solve a critical problem in modern software development: providing Large Language Models (LLMs) with clean, relevant, and structured context from a complex codebase.

Instead of feeding entire repositories to an LLM, you define your project's architectural components as **"Roles"** in a YAML file. The tool analyzes this configuration, finds all related source files and dependencies, and compiles them into a single, well-structured `rolesnap.json` file.

## Key Features

*   **Precision Context for LLMs**: Stop feeding excess code to your AI. Generate focused snapshots containing only the files relevant to a specific feature, service, or architectural layer.
*   **Declarative Architecture**: Define your project's components as "Roles" in a simple YAML file. This configuration becomes a living, executable document of your system's architecture.
*   **Enforce Architectural Boundaries**: By explicitly defining the public API of each module, the tool helps you visualize and maintain a clean, modular, or hexagonal architecture.
*   **Automatic Dependency Resolution**: When one role `imports` another, the tool automatically includes the public API (`external_ports`, `external_domain`) of the dependency, giving the LLM a complete picture without manual copy-pasting.
*   **Structured Output**: The final `rolesnap.json` is neatly organized by categories, making it easy for both humans and machines to parse.

## Core Philosophy: Modular & Hexagonal Architecture

This tool is built on the idea that a well-defined architecture should be enforceable. It encourages a **modular** and **hexagonal** (Ports & Adapters) approach to software design by reifying architectural concepts in the configuration:

*   **A `Role` is a Hexagon**: Each role you define in `rolesnap.yaml` represents a self-contained component, module, or "hexagon."
*   **`external_ports` & `external_domain` are the Ports**: These fields define the explicit public API of your component—its "ports." This is the only surface area that other roles should interact with.
*   **`internal_logic` is the Implementation**: This is the code hidden inside the hexagon. By separating it, you make it clear that no other component should depend on these implementation details.
*   **`imports` are the Adapters**: The `imports` key defines the dependencies between hexagons, ensuring that components only interact through their declared public ports.

By using this tool, your `rolesnap.yaml` becomes a high-level, machine-readable blueprint of your system, helping to prevent architectural drift and making dependencies explicit.

## Installation

It is recommended to install `rolesnap` using `pipx` to avoid dependency conflicts:

```bash
pipx install .
```

Alternatively, you can use `pip` in a virtual environment:

```bash
pip install .
```

## Configuration

The project's main configuration is located in a `rolesnap.yaml` file.

1.  **Copy and Customize**: Copy the example configuration from `examples/rolesnap_example.yaml` to the root of your project and rename it to `rolesnap.yaml`.
2.  **Set the Project Root**: In the `settings` section, define `project_root` with the absolute path to your project's source code.
3.  **Define Your Roles**: In the `roles` section, describe the logical components of your system. For a detailed explanation of each field, refer to the extensive comments inside the `examples/rolesnap_example.yaml` template file itself.

## Usage

The tool is run from the command line using the `rolesnap` command.

### Subcommands

*   `rolesnap full`: Scan the entire project root, respecting excludes.
*   `rolesnap role <name> [--include-utils]`: Scan a single role defined in `rolesnap.yaml`.
*   `rolesnap selfscan`: Scan the `rolesnap` tool itself.
*   `rolesnap validate`: Validate the configuration file.

### Additional Flags:

*   `--config path/to/your/rolesnap.yaml`: Specify an alternative path to the configuration file.
*   `--hide-files`: Create a snapshot that contains only file paths, without their content. Useful for getting a file tree.
*   `--no-banner`: Do not display the startup banner.
*   `--version`: Display the version and exit.
*   `--quiet`: Minimal output, no banner or progress.
*   `--output /path/to/rolesnap.json`: Path to write the snapshot to.
*   `--max-bytes N`: Truncate file contents to N bytes.
*   `--no-color`: Disable color output.

### Validation

You can validate your `rolesnap.yaml` file using the `validate` subcommand:

```bash
rolesnap validate
```

This will check for common errors like cycles in role imports and missing files.

### Tips for Large Repositories

When working with large repositories, you can use the following flags to improve performance and reduce the size of the snapshot:

*   `--hide-files`: Excludes file contents from the snapshot.
*   `--max-bytes N`: Truncates large files to `N` bytes.
*   `--quiet`: Suppresses all non-essential output.

## License

This project is released into the public domain under the [Unlicense](http://unlicense.org/).
