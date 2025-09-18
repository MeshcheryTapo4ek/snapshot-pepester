from __future__ import annotations

from collections.abc import Iterable

from .models import Role


def collect_role_categories(
    roles: dict[str, Role],
    selected_role: str,
    include_utils: bool,
    utils_dirs: list[str],
) -> dict[str, list[str]]:
    """
    Build categorized scan sources for a role using the new schema.

    Categories:
      - Collected Domain        = role.external_domain + sum(import.external_domain)
      - Collected Ports         = role.external_ports  + sum(import.external_ports)
      - Internal Logic          = role.internal_logic (+ utils if include_utils)
      - Base Tasks              = role.base_tasks
      - Collected Base Tasks    = sum(import.base_tasks)
      - Advanced Tasks          = role.advanced_tasks
      - Docs                    = role.docs (own docs only)
    """
    if selected_role not in roles:
        raise ValueError(f"Unknown role '{selected_role}'. Available: {', '.join(sorted(roles))}")

    r: Role = roles[selected_role]

    def add_all(target: set[str], items: Iterable[str]) -> None:
        for it in items:
            if it:
                target.add(it.rstrip("/"))

    # Own sets
    domain_self: set[str] = set()
    ports_self: set[str] = set()
    internal_self: set[str] = set()
    base_self: set[str] = set()
    adv_self: set[str] = set()
    docs_self: set[str] = set()

    add_all(domain_self, r.external_domain)
    add_all(ports_self, r.external_ports)
    add_all(internal_self, r.internal_logic)
    add_all(base_self, r.base_tasks)
    add_all(adv_self, r.advanced_tasks)
    add_all(docs_self, r.docs)
    if include_utils:
        add_all(internal_self, utils_dirs)

    # Imported contributions
    domain_imports: set[str] = set()
    ports_imports: set[str] = set()
    base_imports: set[str] = set()

    for dep_name in r.imports:
        dep = roles.get(dep_name)
        if dep is None:
            raise ValueError(f"Role '{selected_role}' imports unknown role '{dep_name}'")
        add_all(domain_imports, dep.external_domain)
        add_all(ports_imports, dep.external_ports)
        add_all(base_imports, dep.base_tasks)

    return {
        "Collected Domain": sorted(domain_self | domain_imports),
        "Collected Ports": sorted(ports_self | ports_imports),
        "Internal Logic": sorted(internal_self),
        "Base Tasks": sorted(base_self),
        "Collected Base Tasks": sorted(base_imports),
        "Advanced Tasks": sorted(adv_self),
        "Docs": sorted(docs_self),
    }
