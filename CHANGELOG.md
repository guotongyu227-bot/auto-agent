# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.1] - 2026-05-20
### Fixed
- Fixed memory leak in long-running agent sessions (#41)
- Corrected token count estimation for GPT-4o (#39)
- Safe mode now correctly handles keyboard interrupt (#38)

## [0.4.0] - 2026-04-30
### Added
- `AgentPool`: run multiple agents in parallel (#35)
- New `http_post` and `http_patch` built-in tools (#33)
- Task retry logic with exponential backoff (#31)
- `agent.explain()` method to preview planned steps without executing

### Changed
- Improved planner prompt for more reliable multi-step reasoning
- Tool errors now surface cleaner messages to the agent

### Fixed
- Shell tool timeout now respected on Windows (#29)

## [0.3.2] - 2026-03-15
### Fixed
- `file_write` append mode was overwriting on Windows (#27)
- Resolved import error when `requests` not installed (#25)

## [0.3.1] - 2026-03-01
### Fixed
- Pinned `openai>=1.12.0` to avoid breaking change in streaming API
- Fixed crash when tool returns non-string value (#22)

## [0.3.0] - 2026-02-14
### Added
- Task history persistence: save/load history to JSON (#18)
- `@tool` decorator for registering custom tools (#16)
- New example: GitHub PR automation recipe
- Docs: custom tools guide

### Changed
- Agent now streams responses in verbose mode
- Refactored tool registry to support metadata

## [0.2.1] - 2026-01-22
### Fixed
- Fixed circular import between `agent.py` and `tools.py` (#13)
- `directory_list` now handles permission errors gracefully (#12)

## [0.2.0] - 2026-01-08
### Added
- `code_run` tool for executing Python snippets (#9)
- `safe_mode` flag to preview actions before execution (#8)
- Basic test suite with pytest
- Contributing guide

### Changed
- Renamed `execute()` to `run()` for clarity (with deprecation warning)

## [0.1.1] - 2025-12-19
### Fixed
- Missing `requests` in install_requires (#4)
- README typo fixes

## [0.1.0] - 2025-12-10
### Added
- Initial release
- Core agent loop with OpenAI function calling
- Built-in tools: `file_read`, `file_write`, `shell_exec`, `http_get`, `directory_list`
- MIT License
