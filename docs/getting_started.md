# Getting Started with AutoAgent

## Prerequisites

- Python 3.9+
- An OpenAI API key

## Installation

```bash
pip install autoagent-oss
```

## Basic Usage

```python
from autoagent import Agent

agent = Agent(api_key="sk-...")
agent.run("Create a summary of all .py files in this folder")
```

## Safe Mode

Safe mode prompts you to confirm before each action:

```python
agent = Agent(api_key="sk-...", safe_mode=True)
agent.run("Delete all .tmp files in /downloads")
# ⚠️  Safe mode: execute 'shell_exec'? [y/N]:
```

## Environment Variable

Instead of passing the key directly, set:

```bash
export OPENAI_API_KEY=sk-...
```

Then:

```python
agent = Agent()  # picks up from environment
```
