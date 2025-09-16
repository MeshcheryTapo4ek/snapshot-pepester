# Snapshot Pepester

[![Python version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)

A CLI tool for creating role-based, structured snapshots of your codebase, perfect for generating LLM context and enforcing architectural boundaries.

---

## What Is This?

**Snapshot Pepester** is a command-line utility designed to solve a critical problem in modern software development: providing Large Language Models (LLMs) with clean, relevant, and structured context from a complex codebase.

Instead of feeding entire repositories to an LLM, you define your project's architectural components as **"Roles"** in a YAML file. The tool analyzes this configuration, finds all related source files and dependencies, and compiles them into a single, well-structured `snapshot.json` file.

## Key Features

*   **Precision Context for LLMs**: Stop feeding excess code to your AI. Generate focused snapshots containing only the files relevant to a specific feature, service, or architectural layer.
*   **Declarative Architecture**: Define your project's components as "Roles" in a simple YAML file. This configuration becomes a living, executable document of your system's architecture.
*   **Enforce Architectural Boundaries**: By explicitly defining the public API of each module, the tool helps you visualize and maintain a clean, modular, or hexagonal architecture.
*   **Automatic Dependency Resolution**: When one role `imports` another, the tool automatically includes the public API (`external_ports`, `external_domain`) of the dependency, giving the LLM a complete picture without manual copy-pasting.
*   **Structured Output**: The final `snapshot.json` is neatly organized by categories, making it easy for both humans and machines to parse.

## Core Philosophy: Modular & Hexagonal Architecture

This tool is built on the idea that a well-defined architecture should be enforceable. It encourages a **modular** and **hexagonal** (Ports & Adapters) approach to software design by reifying architectural concepts in the configuration:

*   **A `Role` is a Hexagon**: Each role you define in `ta_roles.yaml` represents a self-contained component, module, or "hexagon."
*   **`external_ports` & `external_domain` are the Ports**: These fields define the explicit public API of your component—its "ports." This is the only surface area that other roles should interact with.
*   **`internal_logic` is the Implementation**: This is the code hidden inside the hexagon. By separating it, you make it clear that no other component should depend on these implementation details.
*   **`imports` are the Adapters**: The `imports` key defines the dependencies between hexagons, ensuring that components only interact through their declared public ports.

By using this tool, your `ta_roles.yaml` becomes a high-level, machine-readable blueprint of your system, helping to prevent architectural drift and making dependencies explicit.

## Installation

1.  Clone the repository:
    ```bash
    git clone <your-repo-url>
    cd snapshot-pepester
    ```
2.  Install the package in your virtual environment:
    ```bash
    pip install .
    ```
3.  Verify the installation:
    ```bash
    snapshoter --help
    ```

## Configuration

The project's main configuration is located in the `ta_roles.yaml` file.

1.  **Copy and Customize**: Use the provided `ta_roles.yaml` as a template.
2.  **Set the Project Root**: In the `settings` section, define `project_root` with the absolute path to your project's source code.
3.  **Define Your Roles**: In the `roles` section, describe the logical components of your system. For a detailed explanation of each field, refer to the extensive comments inside the `ta_roles.yaml` template file itself.

## Usage

The tool is run from the command line using the `snapshoter` command.

**1. Create a Snapshot by Role:**

The most common use case. Generates a snapshot based on a role defined in `ta_roles.yaml`.

```bash
# Create a snapshot for the 'auth_service' role and include shared utilities
snapshoter --role auth_service --include-utils
```

**2. Create a Snapshot by Directory or File:**

Useful for quick, ad-hoc snapshots.

```bash
# Include two directories and one specific file in the snapshot
snapshoter --dir services/auth/ --dir shared/utils/ --dir config.py
```

**3. Scan the Tool Itself:**

A mode for meta-analysis and debugging the tool.

```bash
snapshoter --self-scan
```

**4. Scan the Entire Project:**

The default mode if no other flags are provided. Scans the `project_root` while respecting `exclude_dirs`.

```bash
snapshoter
```

### Additional Flags:

*   `--config path/to/roles.yaml`: Specify an alternative path to the configuration file.
*   `--hide-files`: Create a snapshot that contains only file paths, without their content. Useful for getting a file tree.

## License

This project is released into the public domain under the [Unlicense](http://unlicense.org/).
