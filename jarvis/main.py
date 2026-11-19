"""Entry point: python -m jarvis"""
from __future__ import annotations

import argparse
from dataclasses import dataclass

from jarvis import __version__, skills
from jarvis.brain import Brain, OllamaError
from jarvis.config import Config, load_config
from jarvis.voice import Listener, Speaker


@dataclass
class Context:
    config: Config
    brain: Brain


def handle(text: str, ctx: Context) -> tuple[str, bool]:
    """Process one user message. Returns (reply, should_exit)."""
    result = skills.route(text, ctx)
    if result and result.reply is not None:
        return result.reply, result.exit
    context = result.context if result else None
    try:
        return ctx.brain.ask(text, context=context), False
    except OllamaError as e:
        return str(e), False


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Local, offline Jarvis-style assistant")
    parser.add_argument("--config", help="path to config.toml")
    parser.add_argument("--voice", action="store_true", help="use microphone input (Vosk)")
    parser.add_argument("--mute", action="store_true", help="disable spoken replies")
    parser.add_argument("--version", action="version", version=f"jarvis-local {__version__}")
    args = parser.parse_args(argv)

    config = load_config(args.config)
    if args.mute:
        config.voice_output = False
    if args.voice:
        config.voice_input = True

    skills.load_all()
    brain = Brain(config.ollama_url, config.model, config.rendered_system_prompt(), config.history_turns)
    ctx = Context(config, brain)
    speaker = Speaker(config.voice_output, config.voice_rate)

    listener = None
    if config.voice_input:
        try:
            listener = Listener(config.vosk_model_path)
        except RuntimeError as e:
            print(f"[voice] {e}\nFalling back to typing.")

    speaker.say(f"{config.name} online. How can I help, {config.user_name}?")
    while True:
        try:
            text = listener.listen() if listener else input("You: ")
        except (KeyboardInterrupt, EOFError):
            print()
            break
        if not text.strip():
            continue
        reply, should_exit = handle(text, ctx)
        speaker.say(reply)
        if should_exit:
            break


if __name__ == "__main__":
    main()
