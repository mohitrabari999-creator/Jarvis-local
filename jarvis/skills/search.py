"""Optional web search via DuckDuckGo (the only feature that uses the internet).

Off by default. Turn on with `allow_web_search = true` in config.toml.
Results are passed to the local model as context, which then answers.
"""
from jarvis.skills import SkillResult, skill


def ddg_search(query: str, max_results: int = 4) -> list[dict]:
    from ddgs import DDGS  # pip install ddgs

    with DDGS() as d:
        return list(d.text(query, max_results=max_results))


@skill(r"^(?:search(?: the web)?(?: for)?|look up|google) (?P<query>.+)$", name="search",
       help="search for <something> (needs allow_web_search)")
def web_search(match, ctx):
    if not ctx.config.allow_web_search:
        return "Web search is off. Set allow_web_search = true in config.toml to enable it."
    query = match.group("query")
    try:
        results = ddg_search(query)
    except ImportError:
        return "Web search needs the ddgs package: pip install ddgs"
    except Exception as e:
        return f"Search failed: {e}"
    if not results:
        return f"I couldn't find anything for '{query}'."
    context = "\n".join(f"- {r.get('title')}: {r.get('body')}" for r in results)
    return SkillResult(context=f"Web search results for '{query}':\n{context}")
