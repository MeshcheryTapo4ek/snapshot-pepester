from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


@dataclass(frozen=True)
class Role:
    """Role definition (new schema)."""
    help: str = ""
    # External API surface of the role
    external_ports: List[str] = field(default_factory=list)
    external_domain: List[str] = field(default_factory=list)
    # Internal implementation
    internal_logic: List[str] = field(default_factory=list)
    # Task sets
    base_tasks: List[str] = field(default_factory=list)
    advanced_tasks: List[str] = field(default_factory=list)
    # Documentation sources (relative or absolute, arbitrary formats accepted)
    docs: List[str] = field(default_factory=list)
    # Dependencies
    imports: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class Settings:
    """Global settings loaded from YAML."""
    exclude_dirs: Set[str] = field(default_factory=set)
    utils_dirs: List[str] = field(default_factory=list)
    project_root: Optional[str] = None  # absolute filesystem path to the project root
    docs_root: Optional[str] = None     # absolute filesystem path to top-level DOCS folder (sibling to project)


@dataclass(frozen=True)
class Config:
    """Full config bundle."""
    roles: Dict[str, Role] = field(default_factory=dict)
    settings: Settings = field(default_factory=Settings)
