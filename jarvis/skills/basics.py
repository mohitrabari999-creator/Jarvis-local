"""Core skills: time, date, help, reset, exit."""
from datetime import datetime

from jarvis.skills import REGISTRY, SkillResult, skill


@skill(r"^(?:what(?:'s| is) the )?time(?: is it)?(?: now)?$|^what time is it(?: now)?$",
       name="time", help="what time is it")
def tell_time(match, ctx):
    return f"It's {datetime.now().strftime('%I:%M %p').lstrip('0')}."


@skill(r"^(?:what(?:'s| is) )?(?:the |today'?s )?date(?: today)?$|^what day is (?:it|today)$",
       name="date", help="what's the date")
def tell_date(match, ctx):
    return f"Today is {datetime.now().strftime('%A, %d %B %Y')}."


@skill(r"^(help|what can you do)$", name="help", help="list commands")
def show_help(match, ctx):
    lines = [f"  - {s.help}" for s in REGISTRY if s.help]
    return "Here's what I can do directly:\n" + "\n".join(lines) + "\nAnything else, just ask."


@skill(r"^(reset|forget (that|everything)|new conversation)$", name="reset", help="reset the conversation")
def reset(match, ctx):
    ctx.brain.reset()
    return "Okay, starting fresh."


@skill(r"^(exit|quit|goodbye|bye|shut ?down)$", name="exit", help="exit")
def goodbye(match, ctx):
    return SkillResult(reply=f"Goodbye, {ctx.config.user_name}.", exit=True)
