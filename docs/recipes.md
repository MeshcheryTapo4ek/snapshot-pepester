# Configuration Recipes

This page provides practical, copy-pastable examples of `rolesnap.yaml` for common project architectures.

---

## 1. Monorepo / Microservices

This pattern is for projects that contain multiple services or packages within a single repository, often with a shared library.

### Project Structure

```
/path/to/project/
├── packages/
│   ├── auth_service/     # Handles authentication
│   ├── order_service/    # Handles product orders
│   └── shared_kernel/    # Shared DTOs, interfaces, utils
└── docs/
```

### `rolesnap.yaml`

Here, we define three roles. The two services (`auth_service`, `order_service`) both depend on the `shared_kernel`. This means a snapshot for `order_service` will automatically include the public contracts of `shared_kernel`.

```yaml
settings:
  project_root: "/path/to/project"
  exclude_dirs: ["node_modules", ".venv"]

roles:
  # Foundational role with no dependencies
  shared_kernel:
    help: "Core, stable domain models and interfaces used across the application."
    external_ports: ["packages/shared_kernel/ports/"]
    external_domain: ["packages/shared_kernel/dtos/"]
    internal_logic: ["packages/shared_kernel/utils/"]
    imports: []

  # First service, depends on the kernel
  auth_service:
    help: "Handles user authentication and session management."
    external_ports: ["packages/auth_service/controllers/"]
    internal_logic: ["packages/auth_service/"]
    imports:
      - "shared_kernel"

  # Second service, also depends on the kernel
  order_service:
    help: "Handles product orders and inventory."
    external_ports: ["packages/order_service/api/"]
    internal_logic: ["packages/order_service/"]
    imports:
      - "shared_kernel"
```

---

## 2. Hexagonal Architecture (Ports & Adapters)

This architecture cleanly separates the core application logic from infrastructure concerns. `rolesnap` is a natural fit for describing it.

### Project Structure

```
/path/to/project/
└── src/
    └── shipping/
        ├── domain/         # Core business logic and models (agnostic)
        ├── application/    # Use cases that orchestrate the domain
        └── infrastructure/ # Adapters to databases, message queues, etc.
```

### `rolesnap.yaml`

The `domain` is the public contract (`external_domain`), and the `application` layer contains the use cases (`external_ports`). The `infrastructure` is the private implementation detail (`internal_logic`).

```yaml
settings:
  project_root: "/path/to/project"

roles:
  shipping_context:
    help: "Manages the shipping and logistics domain."

    # The public contract is the domain itself.
    external_domain:
      - "src/shipping/domain/"

    # The ports are the application-level use cases.
    external_ports:
      - "src/shipping/application/"

    # The adapters are the implementation details.
    internal_logic:
      - "src/shipping/infrastructure/"

    imports: []
```

---

## 3. Library with a Public API

This is for projects that are published as a package, where you want to distinguish between the public-facing API and internal implementation details.

### Project Structure

```
/path/to/project/
└── my_awesome_lib/
    ├── __init__.py   # Exports the public API
    ├── client.py     # The public client
    └── internal/     # Private helpers and implementation
```

### `rolesnap.yaml`

Here, we explicitly define the public API files in `external_ports` and everything else in `internal_logic`. A snapshot for this role will clearly separate the two, which is perfect for explaining to an LLM how to *use* the library versus how it *works*.

```yaml
settings:
  project_root: "/path/to/project"

roles:
  my_awesome_lib:
    help: "A library for doing awesome things."

    # The public API is what consumers of the library should use.
    external_ports:
      - "my_awesome_lib/__init__.py"
      - "my_awesome_lib/client.py"

    # The rest is considered an implementation detail.
    internal_logic:
      - "my_awesome_lib/internal/"

    imports: []
```
