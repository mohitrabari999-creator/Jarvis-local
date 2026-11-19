from dataclasses import dataclass, field
from unittest.mock import patch

import pytest

from jarvis import skills
from jarvis.config import Config, load_config
from jarvis.main import handle


class FakeBrain:
    def __init__(self):
        self.calls = []
        self.was_reset = False

    def ask(self, text, context=None):
        self.calls.append((text, context))
        return "AI reply"

    def reset(self):
        self.was_reset = True


@dataclass
class Ctx:
    config: Config = field(default_factory=Config)
    brain: FakeBrain = field(default_factory=FakeBrain)


@pytest.fixture(autouse=True, scope="module")
def _load():
    skills.load_all()


@pytest.mark.parametrize("text, expected", [
    ("Hey Jarvis, what time is it?", "what time is it"),
    ("Jarvis please open notepad", "open notepad"),
    ("  Can you   tell me a joke? ", "tell me a joke"),
])
def test_normalize(text, expected):
    assert skills.normalize(text) == expected


@pytest.mark.parametrize("text", ["what time is it", "time", "Jarvis, what's the time?"])
def test_time_skill(text):
    result = skills.route(text, Ctx())
    assert result is not None and result.reply.startswith("It's")


def test_date_skill():
    assert skills.route("what's the date", Ctx()).reply.startswith("Today is")


def test_unknown_goes_to_ai():
    ctx = Ctx()
    reply, should_exit = handle("explain black holes simply", ctx)
    assert reply == "AI reply" and not should_exit
    assert ctx.brain.calls == [("explain black holes simply", None)]


def test_time_question_inside_sentence_goes_to_ai():
    # "time" alone shouldn't hijack a normal question
    assert skills.route("how much time does it take to boil an egg", Ctx()) is None


def test_exit():
    reply, should_exit = handle("goodbye", Ctx())
    assert should_exit


def test_reset():
    ctx = Ctx()
    handle("reset", ctx)
    assert ctx.brain.was_reset


def test_open_known_app_uses_launcher():
    ctx = Ctx(config=Config(apps={"VS Code": "code"}))
    with patch("jarvis.skills.apps.launch") as launch:
        reply = skills.route("open vs code", ctx).reply
    launch.assert_called_once_with("code")
    assert reply == "Opening vs code."


def test_open_unknown_app():
    with patch("jarvis.skills.apps.shutil.which", return_value=None):
        reply = skills.route("open some imaginary app", Ctx()).reply
    assert "don't know how to open" in reply


def test_search_disabled_by_default():
    reply = skills.route("search for python tutorials", Ctx()).reply
    assert "off" in reply


def test_search_passes_results_to_ai():
    ctx = Ctx(config=Config(allow_web_search=True))
    fake = [{"title": "Python", "body": "A programming language"}]
    with patch("jarvis.skills.search.ddg_search", return_value=fake):
        reply, _ = handle("search for python", ctx)
    assert reply == "AI reply"
    assert "A programming language" in ctx.brain.calls[0][1]


def test_load_config(tmp_path):
    p = tmp_path / "config.toml"
    p.write_text('[assistant]\nname = "Friday"\nmodel = "mistral"\n[apps]\nspotify = "spotify"\n')
    cfg = load_config(p)
    assert cfg.name == "Friday" and cfg.model == "mistral"
    assert cfg.apps == {"spotify": "spotify"}
