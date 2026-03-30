# Pagar.me Python SDK

[![Python Version](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/downloads/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Modern Python SDK for integration with the Pagar.me payment gateway (v5).

## Features

- **Asynchronous**: Built on `httpx` for high-performance async calls.
- **Type-safe**: Powered by `Pydantic v2` for data validation and IDE support.
- **Complete**: Support for Customers, Cards, Orders, Charges, and more.

## Installation

```bash
# Using uv
uv add pagarme-python-sdk

# Using pip
pip install pagarme-python-sdk
```

## Quick Start

### Asynchronous (Default)

```python
import asyncio
from pagarme_py import PagarMeClient

async def main():
    async with PagarMeClient(api_key="sk_test_...") as client:
        # Create a customer
        customer = await client.customers.create({
            "name": "Tony Stark",
            "email": "tony@stark.com",
            "document": "12345678909",
            "type": "individual"
        })
        print(f"Created customer: {customer.id}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Synchronous

```python
from pagarme_py import PagarMeSyncClient

def main():
    with PagarMeSyncClient(api_key="sk_test_...") as client:
        # Create a customer
        customer = client.customers.create({
            "name": "Tony Stark",
            "email": "tony@stark.com",
            "document": "12345678909",
            "type": "individual"
        })
        print(f"Created customer: {customer.id}")

if __name__ == "__main__":
    main()
```

## Technologies

- **Python 3.13+**
- **uv** for package and virtual environment management
- **Pydantic v2** for data validation
- **HTTPX** for asynchronous requests
- **Ruff**, **Pyright**, **isort** for code quality
- **Pytest** for automated tests

## Development

To install development dependencies:

```bash
uv sync --all-extras
```

Refer to [.junie/guidelines.md](.junie/guidelines.md) for contribution guidelines.
