# Rolesnap

[![PyPI](https://img.shields.io/pypi/v/rolesnap.svg)](https://pypi.org/project/rolesnap/)
![Python](https://img.shields.io/pypi/pyversions/rolesnap.svg)
[![CI](https://github.com/MeshcheryTapo4ek/snapshot-pepester/actions/workflows/ci.yml/badge.svg)](https://github.com/MeshcheryTapo4ek/snapshot-pepester/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-mkdocs--material-success)](https://meshcherytapo4ek.github.io/snapshot-pepester/)

**Rolesnap creates perfect, structured context for LLMs from your codebase.**

Stop manually copy-pasting files. Define your project's architectural "roles" in a simple YAML file, and let `rolesnap` generate a clean, focused JSON snapshot for you. 

---

## Quickstart

### The 5-Second Way 

Need a snapshot of a single directory? Use the `dir` command.

```bash
# 1. Install the tool
uv tool install rolesnap

# 2. Scan a directory
rolesnap dir /path/to/your/project/src/api
```

That's it. A `rolesnap.json` file is created in `src/api`, ready to be used.

```json
{
  "Scanned Directory": {
    "src/api/main.py": "...",
    "src/api/routes.py": "..."
  }
}
```

### The 5-Command Way (Full Project Configuration)

For more control and to model your entire architecture, use a `rolesnap.yaml` file.


**1. Initialize in your project:**
```bash
cd /path/to/your/project
rolesnap init
```
This creates a template config at `docs/roles/rolesnap.yaml`.

**2. Configure a role:**

Tell `rolesnap` about your `api` service. Edit `docs/roles/rolesnap.yaml`:
```yaml
settings:
  project_root: "/path/to/your/project" # <-- IMPORTANT: Set this!

roles:
  api:
    help: "The main backend API."
    external_domain: ["src/shared/dtos.py"]
    internal_logic: ["src/api/"]
    imports: []
```

**3. Generate the snapshot:**
```bash
# Set the config path for your shell session
export ROLESNAP_CONFIG=./docs/roles/rolesnap.yaml

# This creates rolesnap.json in your project root
rolesnap role api
```

**4. Use the result:**

You get a clean, structured `rolesnap.json` file, ready for your LLM.
```json
{
  "Collected Domain": {
    "src/shared/dtos.py": "class UserDTO:..."
  },
  "Internal Logic": {
    "src/api/main.py": "...",
    "src/api/database.py": "..."
  }
}
```

Now, just copy the contents of `rolesnap.json` and paste it into your prompt.

---

## Why Rolesnap?

- **Stop copy-pasting code.** Let the tool do the boring work.
- **Define your architecture** in a single, executable YAML file.
- **Generate perfect context,** every time, with full dependency awareness.
- **Enforce architectural boundaries** and keep your codebase clean.

> [!TIP]
> For a deep dive into configuration, recipes, and advanced usage, **[read the full documentation](https://meshcherytapo4ek.github.io/snapshot-pepester/)**.

## License

This project is released into the public domain under the [Unlicense](http://unlicense.org/).