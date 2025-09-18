# Configuration

Minimal example:
```yaml
settings:
  project_root: /abs/path/to/project
  exclude_dirs: [".git",".venv","__pycache__"]
roles:
  auth_service:
    help: "Handles auth"
    external_ports: ["services/auth/ports/"]
    external_domain: ["domain/user.py"]
    internal_logic: ["services/auth/"]
    imports: ["shared_kernel"]
  shared_kernel:
    help: "Core models"
    external_ports: ["shared/ports/"]
    external_domain: ["shared/models/"]
    internal_logic: []
    imports: []
```

Recipes: monorepos, hexagonal, microservices, libs — see docs/recipes.md.