# Configuration (`rolesnap.yaml`)

The `rolesnap.yaml` file is the heart of `rolesnap`. It describes your project's architecture so the tool can create precise, role-based snapshots.

## Top-Level Structure

The configuration file has two main keys at its root:

- `settings`: Global configuration for the tool, like project paths and exclusions.
- `roles`: The definitions of your project's architectural components.

```yaml
settings:
  # ... global settings ...

roles:
  # ... role definitions ...
```

---

## The `settings` Block

This section defines global parameters for `rolesnap`.

| Field          | Type        | Required | Description                                                                                                                                 |
|----------------|-------------|----------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `project_root` | `string`    | **Yes**  | The **absolute path** to your project's source code root. All relative paths in the `roles` block are resolved against this directory.        |
| `docs_root`    | `string`    | No       | The **absolute path** to your documentation folder, if it lives outside `project_root`. If provided, paths in a role's `docs` field will be resolved against this. |
| `exclude_dirs` | `list[str]` | No       | A list of directory or file names to globally ignore during scans (e.g., `node_modules`, `.idea`). This extends the built-in exclusion list. |
| `utils_dirs`   | `list[str]` | No       | A list of shared utility/helper directories. These are only included in a snapshot if you use the `--include-utils` flag with `rolesnap role`.      |

---

## The `roles` Block

This is where you define the logical components of your application. A role is a named object containing lists of paths.

| Field             | Type        | Required | Path Type  | Description                                                                                                                                                              |
|-------------------|-------------|----------|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `help`            | `string`    | No       | N/A        | A human-readable description of the role's purpose.                                                                                                                      |
| `external_ports`  | `list[str]` | No       | Relative   | The role's public API or entrypoints (e.g., API controllers, abstract interfaces). **Aggregated** from imported roles into the `Collected Ports` category.                |
| `external_domain` | `list[str]` | No       | Relative   | The role's public models or data structures (e.g., DTOs, core business objects). **Aggregated** from imported roles into the `Collected Domain` category.               |
| `internal_logic`  | `list[str]` | No       | Relative   | The private implementation details of the role. This code should not be imported by other roles. Populates the `Internal Logic` category.                               |
| `base_tasks`      | `list[str]` | No       | Relative   | Foundational tasks or scripts related to the role. Populates the `Base Tasks` category.                                                                                  |
| `advanced_tasks`  | `list[str]` | No       | Relative   | More complex or specialized tasks. Populates the `Advanced Tasks` category.                                                                                              |
| `docs`            | `list[str]` | No       | Relative   | Relevant documentation files. Resolved against `docs_root` if it exists, otherwise `project_root`. Populates the `Docs` category.                                        |
| `imports`         | `list[str]` | No       | Role Names | A list of other roles this role depends on. This is the key to building the dependency graph.                                                                            |


---

## Snapshot Category Semantics

When you run `rolesnap role <name>`, the generated JSON is grouped into categories. Here is how they map to your configuration:

| Snapshot Category      | Origin                                                                                             |
|------------------------|----------------------------------------------------------------------------------------------------|
| `Collected Domain`     | The `external_domain` of the selected role **plus** the `external_domain` of all roles in its `imports` list (recursively). |
| `Collected Ports`      | The `external_ports` of the selected role **plus** the `external_ports` of all roles in its `imports` list (recursively).  |
| `Internal Logic`       | The `internal_logic` of **only** the selected role. If `--include-utils` is used, `settings.utils_dirs` are added here. |
| `Base Tasks`           | The `base_tasks` of **only** the selected role.                                                                    |
| `Collected Base Tasks` | The `base_tasks` of all roles in the `imports` list (recursively).                                                 |
| `Advanced Tasks`       | The `advanced_tasks` of **only** the selected role.                                                                |
| `Docs`                 | The `docs` of **only** the selected role.                                                                          |

---

## Path Resolution

`rolesnap` uses a smart path resolution strategy to avoid common duplication issues. When combining the `project_root` with a relative path from a role definition, it removes any overlapping segments.

**Example:**

- `project_root`: `/home/user/my-project/services`
- Path in role: `services/auth/api`

Instead of incorrectly producing `/home/user/my-project/services/services/auth/api`, the tool identifies that `services` is an overlapping segment and correctly resolves the path to:
`/home/user/my-project/services/auth/api`.

This allows you to use more natural paths in your role definitions.

---

## Validation

`rolesnap` performs several checks to ensure your configuration is valid:

1.  **Import Cycles**: The tool will detect circular dependencies in your role `imports` (e.g., role `A` imports `B`, and `B` imports `A`) and raise an error.
2.  **Missing Paths**: You can use the `rolesnap validate` command to check if all the file and directory paths specified in your roles actually exist on the filesystem. This is useful for catching typos or outdated configurations.

```bash
rolesnap validate
```
