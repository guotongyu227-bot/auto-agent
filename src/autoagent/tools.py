"""
AutoAgent — Built-in Tools and @tool decorator
"""

import os
import subprocess
import requests
import functools


def tool(fn):
    """
    Decorator to register a function as an AutoAgent tool.

    The function's name, docstring, and type hints are used to
    automatically generate the OpenAI function spec.

    Example:
        >>> @tool
        ... def send_slack(channel: str, message: str) -> str:
        ...     '''Send a message to a Slack channel.'''
        ...     ...
        >>> agent.register_tool(send_slack)
    """
    import inspect

    sig = inspect.signature(fn)
    params = {}
    required = []

    for name, param in sig.parameters.items():
        annotation = param.annotation
        if annotation == inspect.Parameter.empty:
            ptype = "string"
        elif annotation == int:
            ptype = "integer"
        elif annotation == bool:
            ptype = "boolean"
        else:
            ptype = "string"

        params[name] = {"type": ptype, "description": name.replace("_", " ").capitalize()}
        if param.default == inspect.Parameter.empty:
            required.append(name)

    spec = {
        "type": "function",
        "function": {
            "name": fn.__name__,
            "description": fn.__doc__ or fn.__name__,
            "parameters": {
                "type": "object",
                "properties": params,
                "required": required,
            },
        },
    }

    fn._tool_spec = {"name": fn.__name__, "fn": fn, "spec": spec}

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    wrapper._tool_spec = fn._tool_spec
    return wrapper


# ─── Built-in tool implementations ────────────────────────────────────────────

def _file_read(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading '{path}': {e}"


def _file_write(path: str, content: str, mode: str = "w") -> str:
    try:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, mode, encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote {len(content)} chars to '{path}'"
    except Exception as e:
        return f"Error writing '{path}': {e}"


def _shell_exec(command: str) -> str:
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=30
        )
        output = (result.stdout + result.stderr).strip()
        return output or "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: command timed out after 30 seconds"
    except Exception as e:
        return f"Error: {e}"


def _http_get(url: str, headers: str = "") -> str:
    try:
        h = {}
        if headers:
            for line in headers.strip().splitlines():
                k, _, v = line.partition(":")
                h[k.strip()] = v.strip()
        resp = requests.get(url, headers=h, timeout=15)
        return resp.text[:4000]
    except Exception as e:
        return f"Error fetching '{url}': {e}"


def _http_post(url: str, body: str, content_type: str = "application/json") -> str:
    try:
        resp = requests.post(
            url,
            data=body,
            headers={"Content-Type": content_type},
            timeout=15,
        )
        return resp.text[:4000]
    except Exception as e:
        return f"Error posting to '{url}': {e}"


def _directory_list(path: str = ".") -> str:
    try:
        items = []
        for entry in sorted(os.scandir(path), key=lambda e: (not e.is_dir(), e.name)):
            kind = "/" if entry.is_dir() else ""
            size = f"  ({entry.stat().st_size} bytes)" if entry.is_file() else ""
            items.append(f"{entry.name}{kind}{size}")
        return "\n".join(items) or "(empty directory)"
    except Exception as e:
        return f"Error listing '{path}': {e}"


def _code_run(code: str) -> str:
    import io
    import contextlib
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(code, {"__builtins__": __builtins__})
        return buf.getvalue() or "(no output)"
    except Exception as e:
        return f"Error: {e}"


def _file_delete(path: str) -> str:
    try:
        os.remove(path)
        return f"Deleted '{path}'"
    except Exception as e:
        return f"Error deleting '{path}': {e}"


def _file_exists(path: str) -> str:
    return str(os.path.exists(path))


# ─── Tool registry ─────────────────────────────────────────────────────────────

def _make_spec(name, description, properties, required):
    return {
        "name": name,
        "fn": None,
        "spec": {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            },
        },
    }


BUILTIN_TOOLS = [
    {
        "name": "file_read",
        "fn": _file_read,
        "spec": {"type": "function", "function": {"name": "file_read", "description": "Read the contents of a file.", "parameters": {"type": "object", "properties": {"path": {"type": "string", "description": "Path to the file"}}, "required": ["path"]}}},
    },
    {
        "name": "file_write",
        "fn": _file_write,
        "spec": {"type": "function", "function": {"name": "file_write", "description": "Write or append content to a file. mode='w' overwrites, mode='a' appends.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}, "mode": {"type": "string", "enum": ["w", "a"]}}, "required": ["path", "content"]}}},
    },
    {
        "name": "file_delete",
        "fn": _file_delete,
        "spec": {"type": "function", "function": {"name": "file_delete", "description": "Delete a file.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
    },
    {
        "name": "file_exists",
        "fn": _file_exists,
        "spec": {"type": "function", "function": {"name": "file_exists", "description": "Check if a file or directory exists.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
    },
    {
        "name": "shell_exec",
        "fn": _shell_exec,
        "spec": {"type": "function", "function": {"name": "shell_exec", "description": "Run a shell command and return its output.", "parameters": {"type": "object", "properties": {"command": {"type": "string", "description": "Shell command to execute"}}, "required": ["command"]}}},
    },
    {
        "name": "http_get",
        "fn": _http_get,
        "spec": {"type": "function", "function": {"name": "http_get", "description": "Fetch a URL via HTTP GET and return the response body.", "parameters": {"type": "object", "properties": {"url": {"type": "string"}, "headers": {"type": "string", "description": "Optional headers, one per line as 'Key: Value'"}}, "required": ["url"]}}},
    },
    {
        "name": "http_post",
        "fn": _http_post,
        "spec": {"type": "function", "function": {"name": "http_post", "description": "Send an HTTP POST request.", "parameters": {"type": "object", "properties": {"url": {"type": "string"}, "body": {"type": "string"}, "content_type": {"type": "string"}}, "required": ["url", "body"]}}},
    },
    {
        "name": "directory_list",
        "fn": _directory_list,
        "spec": {"type": "function", "function": {"name": "directory_list", "description": "List files and directories at a path.", "parameters": {"type": "object", "properties": {"path": {"type": "string", "description": "Directory path (default: current directory)"}}, "required": []}}},
    },
    {
        "name": "code_run",
        "fn": _code_run,
        "spec": {"type": "function", "function": {"name": "code_run", "description": "Execute a Python code snippet and return stdout.", "parameters": {"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}}},
    },
]
