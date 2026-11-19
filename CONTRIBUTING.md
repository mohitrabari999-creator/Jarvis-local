# Contributing to Jarvis Local

Thanks for helping! Beginners are very welcome. Adding a skill is a great first contribution.

## Setup

```bash
git clone https://github.com/mohitrabari999-creator/jarvis-local.git
cd jarvis-local
python -m venv .venv && .venv\Scripts\activate   # or: source .venv/bin/activate
pip install -r requirements.txt pytest
python -m pytest
```

You don't need Ollama running to run the tests.

## Workflow

1. Fork the repo and create a branch: `git checkout -b add-weather-skill`
2. Make your change and add a test in `tests/`
3. Run `python -m pytest`
4. Open a pull request describing what you changed and why

## Writing a skill

- One file per skill (or per group of related skills) in `jarvis/skills/`
- Use `@skill(pattern, help="...")`. The pattern is a regex matched against the
  user's text after it's lowercased and cleaned (e.g. "Hey Jarvis, please" removed)
- Anchor patterns with `^...$` where possible so they don't hijack normal questions
- Return a string to reply, `SkillResult(context=...)` to give the AI extra info,
  or `None` to let the message fall through
- Keep it offline. If a skill needs the internet, make it opt-in via config
- Mock anything that opens apps, plays audio or uses the network in tests

## Code style

- Python 3.11+, type hints where helpful
- Keep functions small and readable; friendly error messages over stack traces

## Reporting bugs

Open an issue with your OS, Python version, Ollama model, what you typed and the full error.
