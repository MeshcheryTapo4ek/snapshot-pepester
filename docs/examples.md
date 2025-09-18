# Examples

Here are some common ways to use `rolesnap`.

## Full Project Snapshot

To get a snapshot of the entire project, use the `full` command.

**Command:**
```bash
rolesnap full
```

**Output:**

This will create a `rolesnap.json` file containing all the files in the project, respecting the `exclude_dirs` in your `rolesnap.yaml`.

```json
{
  "Full Project": {
    "src/rolesnap/cli.py": "...",
    "src/rolesnap/core/engine.py": "...",
    ...
  }
}
```

## Role-based Snapshot

To get a snapshot of a specific role, use the `role` command.

**Command:**
```bash
rolesnap role auth_service
```

**Output:**

This will create a `rolesnap.json` file containing only the files related to the `auth_service` role and its dependencies.

```json
{
  "External Ports": {
    "services/auth/ports/api.py": "..."
  },
  "External Domain": {
    "domain/user_model.py": "..."
  },
  "Internal Logic": {
    "services/auth/main.py": "..."
  },
  "Imported/shared_kernel": {
    "shared/ports/events.py": "..."
  }
}
```
