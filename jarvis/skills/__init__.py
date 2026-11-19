"""Skill system.

A *skill* handles a command directly (open an app, tell the time) without
asking the AI model. To add one, create a file in this folder:

    from jarvis.skills import skill

    @skill(r"^flip a coin$", name="coin", help="flip a coin")
    def flip(match, ctx):
        import random
        return random.choice(["Heads", "Tails"])

Return a string to answer the user, or a `SkillResult` with `context=...` to
hand extra information to the AI model instead of answering directly.
"""
from __future__ import annotations

import importlib
import pkgutil
import re
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class SkillResult:
    reply: str | None = None    # say this directly
    context: str | None = None  # or pass this to the AI as extra context
    exit: bool = False          # stop the assistant


@dataclass
class Skill:
    name: str
    pattern: re.Pattern
    func: Callable[[re.Match, Any], Any]
    help: str = ""


REGISTRY: list[Skill] = []


def skill(pattern: str, name: str | None = None, help: str = ""):
    def decorator(func):
        REGISTRY.append(Skill(name or func.__name__, re.compile(pattern, re.IGNORECASE), func, help))
        return func

    return decorator


def load_all() -> list[Skill]:
    """Import every module in this package so their @skill decorators run."""
    for mod in pkgutil.iter_modules(__path__):
        importlib.import_module(f"{__name__}.{mod.name}")
    return REGISTRY


def normalize(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"^(hey |ok |okay )?(jarvis)[,\s]*", "", text)
    text = re.sub(r"\b(please|can you|could you)\b", "", text)
    return re.sub(r"\s+", " ", text).strip(" ?.!")


def route(text: str, ctx: Any) -> SkillResult | None:
    """Return a SkillResult if a skill matched, else None (send to the AI)."""
    cleaned = normalize(text)
    for s in REGISTRY:
        match = s.pattern.search(cleaned)
        if match:
            result = s.func(match, ctx)
            if result is None:
                continue
            return result if isinstance(result, SkillResult) else SkillResult(reply=str(result))
    return None
