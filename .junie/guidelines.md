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
  - **MANDATORY**: Each logical task or sub-task MUST have its own commit. DO NOT wait until the end of the session to commit everything.
  - Examples of logical steps: "Refactor base client", "Implement SyncCustomerResource", "Update tests for sync mode".
- **Language**: Commit messages and tag messages MUST be in English.
- **Style**: Use the Imperative mood in the subject line (e.g., "Add feature" instead of "Added feature").
- **No Emoticons**: Do NOT use emojis or emoticons in commit messages or tags.
- **Tagging**: When creating a git tag, ALWAYS include a descriptive message using the `-m` flag (e.g., `git tag -a v0.1.0 -m "Release version 0.1.0"`).
- **Co-authorship**: Always include Junie as a co-author using the `--trailer "Co-authored-by: Junie <junie@jetbrains.com>"` flag in commits.

## 7. Versioning and Release Process

### Versioning Best Practices
- **Semantic Versioning (SemVer)**: Follow [SemVer](https://semver.org/) rules (`MAJOR.MINOR.PATCH`).
  - `MAJOR`: Incompatible API changes.
  - `MINOR`: New functionality in a backwards compatible manner.
  - `PATCH`: Backwards compatible bug fixes.
- **Syncing Version**: The version MUST be consistent across:
  - `pyproject.toml`: The source of truth for the package version.
  - `CHANGELOG.md`: Must be updated with the version and release date.
  - `src/pagarme_py/client.py`: The `User-Agent` string should reflect the current version.

### Step-by-Step Release Guide
To create a new version (e.g., `v0.1.3`):

1.  **Update Version with `uv`**:
    Use `uv version` to update `pyproject.toml` and synchronize `uv.lock`.
    ```bash
    uv version 0.1.3
    ```
    Alternatively, to bump automatically:
    ```bash
    uv version --bump patch
    ```
2.  **Update Source Code**:
    Ensure the version in `src/pagarme_py/client.py` (User-Agent) matches the new version.
3.  **Update Changelog**:
    Add a new section in `CHANGELOG.md` for the version, detailing "Added", "Changed", and "Fixed" items.
4.  **Verification**:
    Run all tests and checks:
    ```bash
    uv run pytest
    uv run ruff check .
    uv run pyright
    ```
5.  **Commit Changes**:
    Commit all release-related changes (pyproject.toml, uv.lock, CHANGELOG.md, client.py).
    ```bash
    git add .
    git commit -m "Bump version to 0.1.3 and update CHANGELOG" --trailer "Co-authored-by: Junie <junie@jetbrains.com>"
    ```
6.  **Tagging**:
    Create an annotated tag with a descriptive message:
    ```bash
    git tag -a v0.1.3 -m "Release version 0.1.3"
    ```
7.  **Build and Publish**:
    Generate artifacts and publish to PyPI (manually or via CI/CD):
    ```bash
    uv build
    # Publication is usually handled by GitHub Actions on release creation
    ```

## 8. API Reference
Base the implementation on the official documentation: [Pagar.me API Reference](https://docs.pagar.me/reference/introdu%C3%A7%C3%A3o-1).
