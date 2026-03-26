# Pagar.me Python SDK

[![Python Version](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/downloads/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Modern Python SDK for integration with the Pagar.me payment gateway.

## Technologies

- **Python 3.14**
- **uv** for package and virtual environment management
- **Pydantic v2** for data validation
- **HTTPX** for asynchronous requests
- **Ruff**, **Pyright**, **isort** for code quality
- **Pytest** for automated tests

## Installation

```bash
uv sync
```

## Development

To install development dependencies:

```bash
uv sync --all-extras
```

Refer to [.junie/guidelines.md](.junie/guidelines.md) for contribution guidelines.
