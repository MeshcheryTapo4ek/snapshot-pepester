# CLI Reference

This page provides a detailed reference for all `rolesnap` commands and their arguments.

---

## Global Flags

These flags can be used with any command.

| Flag             | Argument   | Description                                                                                             |
|------------------|------------|---------------------------------------------------------------------------------------------------------|
| `--config`       | `PATH`     | Path to `rolesnap.yaml`. If not set, uses the `ROLESNAP_CONFIG` environment variable.                     |
| `--output`       | `PATH`     | Path to write the snapshot JSON file to. Defaults to `rolesnap.json` in the project root.               |
| `--max-bytes`    | `INTEGER`  | Truncate file contents to a maximum number of bytes. Useful for very large files.                       |
| `--hide-files`   | (none)     | Do not include file contents in the snapshot, only file paths.                                          |
| `--quiet`        | (none)     | Suppress all non-essential output, including the banner and progress bars.                              |
| `--no-color`     | (none)     | Disable colored output.                                                                                 |
| `--no-banner`    | (none)     | Suppress the startup banner.                                                                            |
| `--version`      | (none)     | Display the installed version of `rolesnap` and exit.                                                   |

---

## Commands

### `rolesnap dir <path>`

Scans a single directory with default exclusions, without needing a `rolesnap.yaml` file. This is the quickest way to get a snapshot of a specific part of your project.

**Usage:**
```bash
# Scan the 'src/api' directory
rolesnap dir src/api
```

**Output:**
- A `rolesnap.json` file is created inside `src/api`.

**With Optional Flags:**
```bash
# Scan 'src/api' and save the output to a different file
rolesnap dir src/api --output my-api-snapshot.json
```

**Example JSON Output (`rolesnap.json`):**
```json
{
  "Scanned Directory": {
    "__init__.py": "",
    "api/v1/endpoint.py": "...",
    "main.py": "..."
  }
}
```

---

### `rolesnap init`

Initializes a new configuration file from a template.

**Usage:**
```bash
rolesnap init
```

**Output:**
```
Initializing rolesnap configuration...
Created configuration file at /path/to/your/project/docs/roles/rolesnap.yaml
Please review the file and adjust the paths to your project structure.
```

---

### `rolesnap validate`

Validates the `rolesnap.yaml` file, checking for syntax errors, circular role dependencies, and non-existent paths.

**Usage:**
```bash
# Make sure ROLESNAP_CONFIG is set or use --config
export ROLESNAP_CONFIG=./docs/roles/rolesnap.yaml
rolesnap validate
```

**Output (Success):**
```
Using config from ENV ROLESNAP_CONFIG: /path/to/project/docs/roles/rolesnap.yaml
Config OK. Roles: auth_service, order_service, shared_kernel
```

**Output (Failure):**
```
Using config from ENV ROLESNAP_CONFIG: /path/to/project/docs/roles/rolesnap.yaml
Config valid, but missing paths:
 - packages/auth_service/controllers/
 - packages/order_service/api/
```

---

### `rolesnap role <name>`

Creates a snapshot for a single, specified role, including the public contracts of its dependencies.

**Usage:**
```bash
# Creates rolesnap.json for the 'order_service' role
rolesnap role order_service
```

**With Optional Flags:**
```bash
# Also include shared utility directories in the 'Internal Logic' category
rolesnap role order_service --include-utils
```

**Example JSON Output (`rolesnap.json`):**
```json
{
  "Collected Domain": {
    "packages/shared_kernel/dtos/User.ts": "..."
  },
  "Collected Ports": {},
  "Internal Logic": {
    "packages/order_service/index.ts": "..."
  },
  "Base Tasks": {},
  "Collected Base Tasks": {},
  "Advanced Tasks": {},
  "Docs": {}
}
```

---

### `rolesnap full`

Creates a snapshot of the entire project, respecting the global `exclude_dirs` setting.

**Usage:**
```bash
# Creates rolesnap.json for the full project
rolesnap full --max-bytes 50000
```

**Example JSON Output (`rolesnap.json`):**
```json
{
  "Full Project": {
    "packages/auth_service/index.ts": "...",
    "packages/order_service/index.ts": "...",
    "packages/shared_kernel/dtos/User.ts": "..."
  }
}
```

---

### `rolesnap selfscan`

A diagnostic command that creates a snapshot of the `rolesnap` tool's own source code. This is useful for debugging the tool itself.

**Usage:**
```bash
# Creates rolesnap.json for the tool's own code
rolesnap selfscan
```

**Example JSON Output (`rolesnap.json`):**
```json
{
  "Self-Scan": {
    "src/rolesnap/cli.py": "...",
    "src/rolesnap/core/engine.py": "...",
    "docs/roles/rolesnap.yaml": "..."
  }
}
```
