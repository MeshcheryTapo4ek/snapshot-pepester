from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Role:
    """Role definition (new schema)."""

    help: str = ""
    # External API surface of the role
    external_ports: list[str] = field(default_factory=list)
    external_domain: list[str] = field(default_factory=list)
    # Internal implementation
    internal_logic: list[str] = field(default_factory=list)
    # Task sets
    base_tasks: list[str] = field(default_factory=list)
    advanced_tasks: list[str] = field(default_factory=list)
    # Documentation sources (relative or absolute, arbitrary formats accepted)
    docs: list[str] = field(default_factory=list)
    # Dependencies
    imports: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Settings:
    """Global settings loaded from YAML."""

    exclude_dirs: set[str] = field(default_factory=set)
    utils_dirs: list[str] = field(default_factory=list)
    project_root: str | None = None  # absolute filesystem path to the project root
    docs_root: str | None = (
        None  # absolute filesystem path to top-level DOCS folder (sibling to project)
    )


@dataclass(frozen=True)
class Config:
    """Full config bundle."""

    roles: dict[str, Role] = field(default_factory=dict)
    settings: Settings = field(default_factory=Settings)
