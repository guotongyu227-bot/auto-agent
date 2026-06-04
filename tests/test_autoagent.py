"""
AutoAgent — Tests
"""

import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock
from autoagent.tools import (
    _file_read, _file_write, _file_delete,
    _file_exists, _directory_list, _code_run, tool
)


# ─── File tools ────────────────────────────────────────────────────────────────

def test_file_write_and_read(tmp_path):
    path = str(tmp_path / "test.txt")
    result = _file_write(path, "hello world")
    assert "Successfully" in result

    content = _file_read(path)
    assert content == "hello world"


def test_file_write_append(tmp_path):
    path = str(tmp_path / "append.txt")
    _file_write(path, "line1\n")
    _file_write(path, "line2\n", mode="a")
    content = _file_read(path)
    assert "line1" in content
    assert "line2" in content


def test_file_read_missing():
    result = _file_read("/nonexistent/path/file.txt")
    assert "Error" in result


def test_file_delete(tmp_path):
    path = str(tmp_path / "delete_me.txt")
    _file_write(path, "bye")
    result = _file_delete(path)
    assert "Deleted" in result
    assert not os.path.exists(path)


def test_file_exists(tmp_path):
    path = str(tmp_path / "exists.txt")
    assert _file_exists(path) == "False"
    _file_write(path, "hi")
    assert _file_exists(path) == "True"


def test_directory_list(tmp_path):
    (tmp_path / "file_a.txt").write_text("a")
    (tmp_path / "file_b.txt").write_text("b")
    result = _directory_list(str(tmp_path))
    assert "file_a.txt" in result
    assert "file_b.txt" in result


# ─── Code execution ────────────────────────────────────────────────────────────

def test_code_run_basic():
    result = _code_run("print('hello from code_run')")
    assert "hello from code_run" in result


def test_code_run_math():
    result = _code_run("print(2 ** 10)")
    assert "1024" in result


def test_code_run_error():
    result = _code_run("raise ValueError('oops')")
    assert "Error" in result


# ─── @tool decorator ───────────────────────────────────────────────────────────

def test_tool_decorator():
    @tool
    def greet(name: str) -> str:
        """Greet someone by name."""
        return f"Hello, {name}!"

    assert hasattr(greet, "_tool_spec")
    assert greet._tool_spec["name"] == "greet"
    assert greet("World") == "Hello, World!"


def test_tool_spec_structure():
    @tool
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    spec = add._tool_spec["spec"]
    assert spec["type"] == "function"
    assert "a" in spec["function"]["parameters"]["properties"]
    assert "b" in spec["function"]["parameters"]["properties"]
    assert "a" in spec["function"]["parameters"]["required"]


# ─── Agent (mocked) ────────────────────────────────────────────────────────────

def test_agent_init():
    from autoagent import Agent
    agent = Agent(api_key="sk-test-fake")
    assert agent.model == "gpt-4o"
    assert agent.safe_mode is False
    assert len(agent.tools) > 0


def test_agent_repr():
    from autoagent import Agent
    agent = Agent(api_key="sk-test-fake")
    assert "Agent(" in repr(agent)


def test_agent_no_api_key():
    from autoagent import Agent
    with patch.dict(os.environ, {}, clear=True):
        # Remove OPENAI_API_KEY if set
        os.environ.pop("OPENAI_API_KEY", None)
        with pytest.raises(ValueError, match="API key"):
            Agent()
