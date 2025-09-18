from __future__ import annotations

from typing import Final, Literal

from rich.console import Console
from rich.theme import Theme

THEME: Final = Theme(
    {
        "info": "cyan",
        "success": "green",
        "warn": "yellow",
        "error": "bold red",
        "muted": "dim",
        "path": "magenta",
        "category": "bold blue",
    }
)

console: Console = Console(theme=THEME)


def reinit_console(color_system: Literal["auto", "standard", "256", "truecolor", "windows"] | None = "auto") -> None:
    global console
    console = Console(theme=THEME, color_system=color_system)
