"""
AutoAgent — Custom Tools Example
Shows how to extend AutoAgent with your own tools using the @tool decorator.
"""

from autoagent import Agent, tool
import json
import smtplib


# ── Define custom tools ────────────────────────────────────────────────────────

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city using a public API."""
    import requests
    resp = requests.get(f"https://wttr.in/{city}?format=3", timeout=10)
    return resp.text


@tool
def count_words(text: str) -> str:
    """Count the number of words in a text string."""
    words = text.split()
    return f"{len(words)} words"


@tool
def json_format(json_string: str) -> str:
    """Pretty-print a JSON string with indentation."""
    try:
        parsed = json.loads(json_string)
        return json.dumps(parsed, indent=2)
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {e}"


# ── Register and use ───────────────────────────────────────────────────────────

agent = Agent()
agent.register_tool(get_weather)
agent.register_tool(count_words)
agent.register_tool(json_format)

# Now the agent can use your custom tools
agent.run("What's the weather in Tokyo and San Francisco? Save a comparison to weather.txt")
agent.run('Format this JSON and save it to pretty.json: {"name":"Alice","age":30,"active":true}')
