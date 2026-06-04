"""
AutoAgent — Built-in Tools
"""

import os
import subprocess
import requests


def _file_read(path: str) -> str:
    """Read a file and return its contents."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"


def _file_write(path: str, content: str, mode: str = "w") -> str:
    """Write content to a file."""
    try:
        with open(path, mode, encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {e}"


def _shell_exec(command: str) -> str:
    """Run a shell command and return stdout + stderr."""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=30
        )
        output = result.stdout + result.stderr
        return output.strip() or "(no output)"
    except Exception as e:
        return f"Error: {e}"


def _http_get(url: str) -> str:
    """Fetch a URL and return the response text (truncated)."""
    try:
        resp = requests.get(url, timeout=10)
        return resp.text[:3000]
    except Exception as e:
        return f"Error fetching URL: {e}"


def _directory_list(path: str = ".") -> str:
    """List files in a directory."""
    try:
        items = os.listdir(path)
        return "\n".join(items)
    except Exception as e:
        return f"Error listing directory: {e}"


def _code_run(code: str) -> str:
    """Execute a Python code snippet and return the output."""
    import io
    import contextlib
    stdout = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout):
            exec(code, {})
        return stdout.getvalue() or "(no output)"
    except Exception as e:
        return f"Error: {e}"


BUILTIN_TOOLS = [
    {
        "name": "file_read",
        "fn": _file_read,
        "spec": {
            "type": "function",
            "function": {
                "name": "file_read",
                "description": "Read the contents of a file.",
                "parameters": {
                    "type": "object",
                    "properties": {"path": {"type": "string", "description": "File path to read"}},
                    "required": ["path"]
                }
            }
        }
    },
    {
        "name": "file_write",
        "fn": _file_write,
        "spec": {
            "type": "function",
            "function": {
                "name": "file_write",
                "description": "Write content to a file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "content": {"type": "string"},
                        "mode": {"type": "string", "enum": ["w", "a"], "default": "w"}
                    },
                    "required": ["path", "content"]
                }
            }
        }
    },
    {
        "name": "shell_exec",
        "fn": _shell_exec,
        "spec": {
            "type": "function",
            "function": {
                "name": "shell_exec",
                "description": "Run a shell command.",
                "parameters": {
                    "type": "object",
                    "properties": {"command": {"type": "string"}},
                    "required": ["command"]
                }
            }
        }
    },
    {
        "name": "http_get",
        "fn": _http_get,
        "spec": {
            "type": "function",
            "function": {
                "name": "http_get",
                "description": "Fetch a URL and return its content.",
                "parameters": {
                    "type": "object",
                    "properties": {"url": {"type": "string"}},
                    "required": ["url"]
                }
            }
        }
    },
    {
        "name": "directory_list",
        "fn": _directory_list,
        "spec": {
            "type": "function",
            "function": {
                "name": "directory_list",
                "description": "List files in a directory.",
                "parameters": {
                    "type": "object",
                    "properties": {"path": {"type": "string", "default": "."}},
                    "required": []
                }
            }
        }
    },
    {
        "name": "code_run",
        "fn": _code_run,
        "spec": {
            "type": "function",
            "function": {
                "name": "code_run",
                "description": "Execute a Python code snippet.",
                "parameters": {
                    "type": "object",
                    "properties": {"code": {"type": "string"}},
                    "required": ["code"]
                }
            }
        }
    },
]
