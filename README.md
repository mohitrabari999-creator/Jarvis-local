# Jarvis Local 🤖

**A Jarvis-style personal AI assistant that runs 100% on your own computer.**
No cloud, no API keys, no subscription. Your conversations never leave your PC.

Powered by [Ollama](https://ollama.com) (Llama 3.1 by default), with offline
text-to-speech and optional offline voice recognition.

```
Jarvis online. How can I help, sir?
You: open notepad
Opening notepad.
You: explain recursion like I'm 12
Recursion is when a function solves a problem by calling a smaller version of itself...
```

## Features

- 🧠 **Local AI brain** – chat with any Ollama model (Llama 3.1, Mistral, Qwen, Phi...)
- 🗣️ **Talks back** – offline text-to-speech via `pyttsx3`
- 🎙️ **Listens (optional)** – offline speech recognition via [Vosk](https://alphacephei.com/vosk/)
- 🚀 **Opens apps & websites** – "open calculator", "open youtube", plus your own shortcuts
- 🧩 **Skills system** – add new commands with one small Python file
- 🔎 **Web search (opt-in)** – DuckDuckGo results summarized by the local model
- 💻 Windows, macOS and Linux

## Requirements

- Python 3.11+
- [Ollama](https://ollama.com/download)
- A GPU with ~6 GB VRAM is recommended for `llama3.1:8b` (smaller models like `llama3.2:3b` run on most laptops)

## Quick start

```bash
# 1. Get a model
ollama pull llama3.1:8b

# 2. Get the code
git clone https://github.com/mohitrabari999-creator/jarvis-local.git
cd jarvis-local
python -m venv .venv
.venv\Scripts\activate          # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt

# 3. Configure (optional)
copy config.example.toml config.toml    # macOS/Linux: cp

# 4. Run
python -m jarvis
```

Options: `--mute` (no speech), `--voice` (microphone input), `--config path/to/config.toml`.

### Voice input (optional)

```bash
pip install vosk sounddevice
```

Download a small English model (~40 MB) from the
[Vosk models page](https://alphacephei.com/vosk/models), unzip it into a
`models/` folder, then run `python -m jarvis --voice`.

## Commands

| Say / type | What happens |
|---|---|
| `open notepad`, `open youtube` | Opens an app or website |
| `what time is it`, `what's the date` | Answers instantly |
| `search for <topic>` | Web search (when enabled) + AI summary |
| `reset` | Clears the conversation memory |
| `help` | Lists commands |
| `bye` | Exits |
| anything else | Answered by the local AI model |

Add your own app shortcuts under `[apps]` in `config.toml`.

## Adding a skill

Create a file in `jarvis/skills/`, e.g. `jarvis/skills/coin.py`:

```python
import random
from jarvis.skills import skill

@skill(r"^flip a coin$", help="flip a coin")
def flip(match, ctx):
    return random.choice(["Heads!", "Tails!"])
```

That's it. It's loaded automatically. See [CONTRIBUTING.md](CONTRIBUTING.md).

## How it works

```
 your words ─▶ skill router ─┬─▶ matched a skill? ─▶ instant answer / action
                             └─▶ no ─▶ Ollama (local LLM) ─▶ reply
                                                     │
                                          pyttsx3 speaks the reply
```

## Roadmap

Ideas where help is very welcome:

- [ ] Wake word ("Hey Jarvis") detection
- [ ] Whisper-based speech recognition option
- [ ] Reminders and timers
- [ ] Volume / media / brightness control
- [ ] System info skill (CPU, RAM, battery)
- [ ] Simple GUI window
- [ ] Hindi and other language support

## Contributing

Contributions of all sizes are welcome: new skills, bug fixes, docs, translations.
Check issues labeled **good first issue** and read [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
