"""Load settings from config.toml (falls back to sensible defaults)."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_PATH = Path(__file__).resolve().parent.parent / "config.toml"


@dataclass
class Config:
    name: str = "Jarvis"
    user_name: str = "sir"
    ollama_url: str = "http://localhost:11434"
    model: str = "llama3.1:8b"
    system_prompt: str = (
        "You are {name}, a helpful, concise personal assistant running fully "
        "offline on the user's computer. Address the user as {user_name}. "
        "Keep spoken answers short (1-3 sentences) unless asked for detail."
    )
    history_turns: int = 10
    voice_output: bool = True
    voice_rate: int = 180
    voice_input: bool = False
    vosk_model_path: str = "models/vosk-model-small-en-us-0.15"
    allow_web_search: bool = False
    apps: dict[str, str] = field(default_factory=dict)

    def rendered_system_prompt(self) -> str:
        return self.system_prompt.format(name=self.name, user_name=self.user_name)


def load_config(path: Path | str | None = None) -> Config:
    path = Path(path) if path else DEFAULT_PATH
    cfg = Config()
    if not path.exists():
        return cfg
    with open(path, "rb") as f:
        data = tomllib.load(f)
    # Sections like [assistant] or [voice] are flattened; [apps] stays a dict.
    flat: dict = {}
    for key, value in data.items():
        if isinstance(value, dict) and key != "apps":
            flat.update(value)
        else:
            flat[key] = value
    for key, value in flat.items():
        if hasattr(cfg, key):
            setattr(cfg, key, value)
    return cfg
