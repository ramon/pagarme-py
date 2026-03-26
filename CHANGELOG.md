# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-03-26

### Added
- Initial release of the Pagar.me Python SDK.
- Core client with asynchronous support using `httpx`.
- Customer management (CRUD and Card sub-resource).
- Order and Charge management.
- Multi-payment method support (Credit Card, Boleto, Pix).
- Pydantic v2 models for all resources.
- Support for full phone parsing.
