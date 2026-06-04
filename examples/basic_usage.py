"""
AutoAgent — Example Usage
"""

from autoagent import Agent

agent = Agent(api_key="your-openai-api-key")

# Example 1: File automation
agent.run("Create a file called hello.txt that says 'Hello from AutoAgent!'")

# Example 2: Multi-step task
agent.run(
    "List all files in the current directory, "
    "then create a file called inventory.txt listing each file and its size"
)

# Example 3: Web + file
agent.run(
    "Fetch https://api.github.com/repos/openai/openai-python "
    "and save the repo description and star count to github_info.txt"
)
