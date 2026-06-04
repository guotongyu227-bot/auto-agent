"""
AutoAgent — Automation Recipes
A collection of ready-to-use automation examples.
"""

from autoagent import Agent

agent = Agent()  # uses OPENAI_API_KEY from environment

# ── Recipe 1: Daily standup summary ──────────────────────────────────────────
# Reads your git log and writes a standup summary
agent.run(
    "Run 'git log --oneline --since=yesterday' and write a concise standup summary "
    "of what was worked on to standup.md"
)

# ── Recipe 2: Clean up temp files ────────────────────────────────────────────
agent.run(
    "Find all .tmp and .log files in the current directory that are older than 7 days "
    "and delete them. Tell me how many were removed."
)

# ── Recipe 3: Project health check ───────────────────────────────────────────
agent.run(
    "List all Python files in this project, check if each has a corresponding test file, "
    "and write a coverage gap report to coverage_gaps.md"
)

# ── Recipe 4: README update ───────────────────────────────────────────────────
agent.run(
    "Read setup.py to get the current version, then update the version badge in README.md "
    "to match it."
)

# ── Recipe 5: Dependency audit ────────────────────────────────────────────────
agent.run(
    "Run 'pip list --outdated' and save the results to outdated_packages.txt, "
    "then summarize which packages have major version updates available."
)
