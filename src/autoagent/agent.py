"""
AutoAgent — Core Agent Loop
"""

import os
import json
import logging
from typing import Optional, List
from openai import OpenAI

logger = logging.getLogger(__name__)


class Agent:
    """
    AutoAgent: Execute tasks described in natural language using OpenAI function calling.

    Args:
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
        model: OpenAI model to use. Default: gpt-4o.
        safe_mode: If True, prompt user to confirm each tool call before executing.
        verbose: If True, print detailed step-by-step logs.
        max_retries: Number of retries on tool failure before giving up.

    Example:
        >>> agent = Agent(api_key="sk-...")
        >>> agent.run("Create a file called hello.txt with today's date")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o",
        safe_mode: bool = False,
        verbose: bool = True,
        max_retries: int = 2,
    ):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key required. Pass api_key= or set the OPENAI_API_KEY environment variable."
            )
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.safe_mode = safe_mode
        self.verbose = verbose
        self.max_retries = max_retries
        self.tools: List[dict] = []
        self.history: List[dict] = []
        self._register_builtin_tools()

    def _register_builtin_tools(self):
        from autoagent.tools import BUILTIN_TOOLS
        for t in BUILTIN_TOOLS:
            self.tools.append(t)

    def register_tool(self, fn):
        """
        Register a custom tool function decorated with @tool.

        Args:
            fn: A function decorated with @autoagent.tool.

        Example:
            >>> @tool
            ... def ping(host: str) -> str:
            ...     '''Ping a host and return latency.'''
            ...     import subprocess
            ...     return subprocess.check_output(["ping", "-c", "1", host]).decode()
            >>> agent.register_tool(ping)
        """
        if not hasattr(fn, "_tool_spec"):
            raise ValueError("Function must be decorated with @tool before registering.")
        self.tools.append(fn._tool_spec)

    def explain(self, task: str) -> str:
        """
        Preview what the agent plans to do for a task without executing any tools.

        Args:
            task: Natural language task description.

        Returns:
            A plain-text explanation of the planned steps.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are AutoAgent. Given a task, explain step by step what you would do "
                        "and which tools you would use. Do NOT execute anything — just explain."
                    ),
                },
                {"role": "user", "content": f"Task: {task}"},
            ],
        )
        return response.choices[0].message.content

    def run(self, task: str, max_steps: int = 15) -> str:
        """
        Execute a natural language task.

        Args:
            task: Plain English description of what to do.
            max_steps: Maximum reasoning steps before stopping.

        Returns:
            Final result as a string.

        Raises:
            RuntimeError: If the agent exceeds max_steps without completing.
        """
        if self.verbose:
            print(f"\n🤖 AutoAgent [{self.model}] — Task: {task}\n{'─' * 60}")

        messages = [
            {
                "role": "system",
                "content": (
                    "You are AutoAgent, an AI that executes real developer tasks using available tools. "
                    "Think step by step. Use tools as needed. When the task is complete, "
                    "provide a clear summary of what was done."
                ),
            },
            {"role": "user", "content": task},
        ]

        tool_specs = [t["spec"] for t in self.tools]

        for step in range(max_steps):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tool_specs,
                tool_choice="auto",
            )

            msg = response.choices[0].message
            messages.append(msg)

            if msg.tool_calls:
                for call in msg.tool_calls:
                    tool_name = call.function.name
                    args = json.loads(call.function.arguments)

                    if self.verbose:
                        print(f"  🔧 {tool_name}({', '.join(f'{k}={repr(v)[:40]}' for k, v in args.items())})")

                    if self.safe_mode:
                        confirm = input(f"  ⚠️  Execute '{tool_name}'? [y/N]: ")
                        if confirm.strip().lower() != "y":
                            result = "Action skipped by user in safe mode."
                        else:
                            result = self._call_tool_with_retry(tool_name, args)
                    else:
                        result = self._call_tool_with_retry(tool_name, args)

                    if self.verbose:
                        preview = str(result)[:120].replace("\n", " ")
                        print(f"     → {preview}{'…' if len(str(result)) > 120 else ''}")

                    messages.append({
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": str(result),
                    })
            else:
                final = msg.content
                if self.verbose:
                    print(f"\n✅ Done: {final}\n")
                self.history.append({"task": task, "result": final, "steps": step + 1})
                return final

        raise RuntimeError(f"Agent did not complete the task within {max_steps} steps.")

    def _call_tool_with_retry(self, name: str, args: dict) -> str:
        for attempt in range(self.max_retries + 1):
            try:
                return self._call_tool(name, args)
            except Exception as e:
                if attempt < self.max_retries:
                    logger.warning(f"Tool '{name}' failed (attempt {attempt + 1}): {e}. Retrying...")
                else:
                    return f"Tool '{name}' failed after {self.max_retries + 1} attempts: {e}"

    def _call_tool(self, name: str, args: dict) -> str:
        for t in self.tools:
            if t["name"] == name:
                return t["fn"](**args)
        return f"Unknown tool: '{name}'"

    def save_history(self, path: str) -> None:
        """Save task history to a JSON file."""
        with open(path, "w") as f:
            json.dump(self.history, f, indent=2)
        print(f"History saved to {path}")

    def load_history(self, path: str) -> None:
        """Load task history from a JSON file."""
        with open(path) as f:
            self.history = json.load(f)

    def __repr__(self):
        return f"Agent(model={self.model!r}, tools={len(self.tools)}, safe_mode={self.safe_mode})"
