# Roadmap

This page outlines the planned features and future direction for `rolesnap`. Community feedback and contributions are welcome!

---

## 1. CLI Autocompletion

- **Goal**: To speed up CLI usage and reduce errors by providing shell autocompletion for commands, flags, and role names.
- **Command**: `rolesnap --install-completion [bash|zsh|fish|powershell]`
- **Features**:
    - Autocomplete for subcommands (`full`, `role`, etc.).
    - Autocomplete for flags (`--include-utils`, `--output`, etc.).
    - Dynamic autocompletion for role names by reading `rolesnap.yaml`.
    - A corresponding `--uninstall-completion` command.

---

## 2. Pre-built Templates for `init`

- **Goal**: To lower the barrier to entry by providing ready-to-use configuration templates for popular frameworks and architectures.
- **Command**: `rolesnap init --template [monorepo|hexagonal|django|fastapi|react]`
- **Features**:
    - A collection of curated `.yaml` templates bundled with the tool.
    - The `init` command will generate a `rolesnap.yaml` based on the selected template.
    - Optional flags like `--force` to overwrite existing files and `--with-docs` to generate a helpful `README.md` alongside the config.

---

## 3. Role Dependency Graph

- **Goal**: To provide a visual representation of the project's architecture, making it easier to understand dependencies and review architectural boundaries.
- **Command**: `rolesnap graph --format [svg|png] --out rolesnap-graph.svg`
- **Features**:
    - Generate a directed graph where nodes are roles and edges represent `imports`.
    - Render the graph to an image file (`.svg` or `.png`).
    - The initial version will use Graphviz (dot), with a potential fallback to an ASCII graph if Graphviz is not installed.
    - The output image will be suitable for embedding in documentation or PRs.
