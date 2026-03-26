# Pagar.me Python SDK Guidelines

This document establishes the development guidelines for the Pagar.me API Python SDK.

## 1. Technology Stack
- **Language**: Python 3.13+
- **Package Management**: [uv](https://github.com/astral-sh/uv).
- **Data Modeling**: [Pydantic v2](https://docs.pydantic.dev/) for validation and serialization.
- **HTTP Client**: [HTTPX](https://www.python-httpx.org/) (support for synchronous and asynchronous calls).
- **Testing**: [Pytest](https://docs.pytest.org/).
- **Linting/Formatting**: [Ruff](https://beta.ruff.rs/) (replacing Flake8 and Black).
- **Import Sorting**: [isort](https://pycqa.github.io/isort/).
- **Type Checking**: [Pyright](https://github.com/microsoft/pyright).

## 2. Project Structure
The source code must be organized under the `src/pagarme_py` directory:
- `models/`: Pydantic definitions for Requests and Responses.
- `resources/`: Endpoint implementation (e.g., `customers`, `transactions`, `orders`).
- `client.py`: Main entry class for the SDK.
- `exceptions.py`: Handling of API-specific errors.

## 3. Coding Standards
- **Language**: All documentation, docstrings, and comments MUST be in English.
- **Type Hinting**: Mandatory in all functions, methods, and public variables.
- **Asynchrony**: The SDK should preferably provide an asynchronous interface using `httpx.AsyncClient`.
- **Naming**: Follow `snake_case` for functions/variables and `PascalCase` for classes, as per [PEP 8](https://peps.python.org/pep-0008/).
- **Documentation**: Use Google/Sphinx-style Docstrings.

## 4. Testing
- All tests must be in the `tests/` directory.
- Use `pytest` and `pytest-asyncio`.
- Mock network calls using `pytest-httpx` or `unittest.mock`.
- Minimum desired coverage: 80%.

## 5. Development Workflow
1. Keep the environment updated: `uv sync --all-extras`.
2. Run linting/formatting before each commit:
   ```bash
   uv run ruff check . --fix
   uv run isort .
   uv run pyright
   ```
3. Run tests: `uv run pytest`.

## 6. Git Commit and Tagging Best Practices
- **Commit History**: The agent MUST commit changes as they are completed, following logical steps.
- **Language**: Commit messages and tag messages MUST be in English.
- **Style**: Use the Imperative mood in the subject line (e.g., "Add feature" instead of "Added feature").
- **No Emoticons**: Do NOT use emojis or emoticons in commit messages or tags.
- **Tagging**: When creating a git tag, ALWAYS include a descriptive message using the `-m` flag (e.g., `git tag -a v0.1.0 -m "Release version 0.1.0"`).
- **Co-authorship**: Always include Junie as a co-author using the `--trailer "Co-authored-by: Junie <junie@jetbrains.com>"` flag in commits.

## 7. API Reference
Base the implementation on the official documentation: [Pagar.me API Reference](https://docs.pagar.me/reference/introdu%C3%A7%C3%A3o-1).
