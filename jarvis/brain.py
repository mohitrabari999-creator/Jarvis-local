"""Talks to a local Ollama server. No cloud APIs, no API keys."""
from __future__ import annotations

import requests


class OllamaError(RuntimeError):
    pass


class Brain:
    def __init__(self, url: str, model: str, system_prompt: str, history_turns: int = 10):
        self.url = url.rstrip("/")
        self.model = model
        self.system_prompt = system_prompt
        self.history_turns = history_turns
        self.history: list[dict[str, str]] = []

    def _messages(self, user_text: str, context: str | None = None) -> list[dict[str, str]]:
        messages = [{"role": "system", "content": self.system_prompt}]
        messages += self.history[-self.history_turns * 2 :]
        content = user_text if not context else f"{user_text}\n\nUseful context:\n{context}"
        messages.append({"role": "user", "content": content})
        return messages

    def ask(self, user_text: str, context: str | None = None) -> str:
        try:
            resp = requests.post(
                f"{self.url}/api/chat",
                json={"model": self.model, "messages": self._messages(user_text, context), "stream": False},
                timeout=120,
            )
            resp.raise_for_status()
        except requests.ConnectionError as e:
            raise OllamaError(
                "Can't reach Ollama. Is it running? Start it with `ollama serve` "
                f"and make sure you've pulled the model: `ollama pull {self.model}`"
            ) from e
        except requests.HTTPError as e:
            raise OllamaError(f"Ollama returned an error: {resp.text[:200]}") from e

        reply = resp.json().get("message", {}).get("content", "").strip()
        self.history.append({"role": "user", "content": user_text})
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def reset(self) -> None:
        self.history.clear()
