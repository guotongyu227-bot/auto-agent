# 🤖 AutoAgent — Natural Language Task Automation

> Automate your daily developer workflows using plain English. No scripts. No boilerplate.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenAI](https://img.shields.io/badge/Powered%20by-OpenAI-black.svg)](https://openai.com)

---

## ✨ What is AutoAgent?

AutoAgent is an open-source Python framework that lets you describe tasks in natural language and execute them automatically. It uses OpenAI's API to interpret instructions and run real actions — file operations, web requests, code generation, shell commands, and more.

**Instead of writing:**
```bash
find . -name "*.log" -mtime +7 -delete && echo "Done cleaning logs"
```

**You write:**
```python
agent.run("Delete all log files older than 7 days and tell me what was removed")
```

---

## 🚀 Features

- 🗣️ **Natural language interface** — describe tasks the way you think
- 🔧 **Built-in tools** — file system, shell, HTTP, code execution
- 🔁 **Multi-step reasoning** — handles complex, multi-stage workflows
- 🧩 **Extensible** — add your own tools with a simple decorator
- 📋 **Task history** — log and replay past automations
- 🔒 **Safe mode** — preview actions before executing

---

## 📦 Installation

```bash
pip install autoagent-oss
```

Or from source:

```bash
git clone https://github.com/guotongyu227-bot/auto-agent
cd auto-agent
pip install -e .
```

---

## ⚡ Quick Start

```python
from autoagent import Agent

agent = Agent(api_key="your-openai-api-key")

# Simple file task
agent.run("Create a file called notes.txt with today's date as a header")

# Multi-step task
agent.run("Find all Python files in this directory, count the lines in each, and save a summary to report.txt")

# Web + file task
agent.run("Fetch the latest GitHub trending repos for Python and save the top 5 to trending.md")
```

---

## 🛠️ Built-in Tools

| Tool | Description |
|------|-------------|
| `file_read` | Read file contents |
| `file_write` | Write or append to files |
| `shell_exec` | Run shell commands |
| `http_get` | Make HTTP GET requests |
| `code_run` | Execute Python code snippets |
| `directory_list` | List files in a directory |

---

## 🧩 Adding Custom Tools

```python
from autoagent import Agent, tool

agent = Agent(api_key="your-openai-api-key")

@tool
def send_slack_message(channel: str, message: str) -> str:
    """Send a message to a Slack channel."""
    # your implementation here
    return f"Message sent to {channel}"

agent.register_tool(send_slack_message)
agent.run("Send a message to #dev-team saying the deployment is complete")
```

---

## 📁 Project Structure

```
auto-agent/
├── src/
│   ├── autoagent/
│   │   ├── __init__.py
│   │   ├── agent.py        # Core agent loop
│   │   ├── tools.py        # Built-in tools
│   │   ├── planner.py      # Task planning logic
│   │   └── memory.py       # Task history & context
├── examples/
│   ├── basic_usage.py
│   ├── custom_tools.py
│   └── automation_recipes.py
├── docs/
│   └── getting_started.md
├── tests/
├── README.md
├── setup.py
└── LICENSE
```

---

## 🗺️ Roadmap

- [ ] Web UI dashboard for task management
- [ ] Scheduled/recurring task support
- [ ] Multi-agent collaboration
- [ ] Plugin marketplace
- [ ] Local LLM support (Ollama, LM Studio)

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or pull request.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

Built on top of the [OpenAI API](https://platform.openai.com/docs). Inspired by the open-source agent community.
