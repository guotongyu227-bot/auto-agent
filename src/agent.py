"""
AutoAgent — Natural Language Task Automation
Core agent module
"""

import os
import json
from typing import Optional
from openai import OpenAI


class Agent:
    """
    AutoAgent: Run tasks described in natural language using OpenAI function calling.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o", safe_mode: bool = False):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY or pass api_key=")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.safe_mode = safe_mode
        self.tools = []
        self.history = []
        self._register_builtin_tools()

    def _register_builtin_tools(self):
        from autoagent.tools import BUILTIN_TOOLS
        for t in BUILTIN_TOOLS:
            self.tools.append(t)

    def register_tool(self, fn):
        """Register a custom tool decorated with @tool."""
        self.tools.append(fn._tool_spec)

    def run(self, task: str, max_steps: int = 10) -> str:
        """
        Execute a natural language task.

        Args:
            task: Plain English description of what to do.
            max_steps: Max number of reasoning steps before stopping.

        Returns:
            Final result as a string.
        """
        print(f"\n🤖 AutoAgent starting task: {task}\n")
        messages = [
            {
                "role": "system",
                "content": (
                    "You are AutoAgent, an AI that executes real tasks using available tools. "
                    "Break down the task into steps, use tools as needed, and report the final result clearly."
                )
            },
            {"role": "user", "content": task}
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

                    print(f"  🔧 Using tool: {tool_name}({args})")

                    if self.safe_mode:
                        confirm = input(f"  ⚠️  Safe mode: execute '{tool_name}'? [y/N]: ")
                        if confirm.lower() != "y":
                            result = "Action skipped by user."
                        else:
                            result = self._call_tool(tool_name, args)
                    else:
                        result = self._call_tool(tool_name, args)

                    messages.append({
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": str(result)
                    })
            else:
                # Final answer
                final = msg.content
                print(f"\n✅ Done: {final}\n")
                self.history.append({"task": task, "result": final})
                return final

        return "Max steps reached without completion."

    def _call_tool(self, name: str, args: dict) -> str:
        for t in self.tools:
            if t["name"] == name:
                return t["fn"](**args)
        return f"Tool '{name}' not found."
