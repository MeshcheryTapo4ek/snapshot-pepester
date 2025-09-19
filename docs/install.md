# Installation

`rolesnap` is a Python CLI tool and can be installed using `uv`.

## Standalone Tool (Recommended)

For most users, we recommend installing `rolesnap` as a standalone tool using `uv tool install`. This keeps its dependencies isolated from your projects.

```bash
# Install the latest version
uv tool install rolesnap

# Verify the installation
uv run rolesnap --version
```

## In-Project Installation

If you want to pin `rolesnap` to a specific version for a single project, you can add it to your project's dependencies.

```bash
# Add rolesnap to your project's virtual environment
uv add rolesnap

# Run it using the uv run command
uv run rolesnap --version
```
