# Contributing to AutoAgent

Thank you for your interest in contributing! AutoAgent is a community-driven project and we welcome contributions of all kinds — bug fixes, new tools, documentation, and ideas.

## Getting Started

### 1. Fork and clone the repo

```bash
git clone https://github.com/your-username/auto-agent
cd auto-agent
```

### 2. Set up your development environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### 3. Run the tests

```bash
pytest tests/
```

---

## How to Contribute

### Reporting Bugs

Please open a [GitHub Issue](https://github.com/guotongyu227-bot/auto-agent/issues) and include:
- Python version and OS
- AutoAgent version (`pip show autoagent-oss`)
- Minimal reproduction case
- Expected vs actual behavior

### Suggesting Features

Open an issue with the `enhancement` label. Describe the use case and why it would benefit others.

### Submitting a Pull Request

1. Create a branch: `git checkout -b feature/my-feature`
2. Make your changes with clear, focused commits
3. Add or update tests in `tests/`
4. Update `docs/` and `CHANGELOG.md` if relevant
5. Open a PR with a clear description

---

## Adding a Custom Tool

The easiest contribution is a new built-in tool. Tools live in `src/autoagent/tools.py`.

Each tool needs:
1. A Python function
2. An OpenAI function spec
3. An entry in `BUILTIN_TOOLS`

Example:

```python
def _send_email(to: str, subject: str, body: str) -> str:
    """Send an email using SMTP."""
    # implementation
    return f"Email sent to {to}"
```

---

## Code Style

- Follow PEP 8
- Use type hints where possible
- Write docstrings for all public functions
- Keep functions small and focused

We use `black` for formatting:

```bash
black src/ tests/
```

---

## Code of Conduct

Be kind, respectful, and constructive. We follow the [Contributor Covenant](https://www.contributor-covenant.org/).
