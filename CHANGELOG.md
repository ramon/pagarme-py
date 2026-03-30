# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-03-30

### Added
- New `PagarMeSyncClient` for synchronous API calls.
- Synchronous versions of all resources (`SyncCustomerResource`, `SyncOrderResource`, `SyncChargeResource`).
- `BasePagarMeClient` to share configuration and logic between sync and async modes.

### Changed
- Refactored internal client architecture to support dual-mode (sync/async).
- Updated User-Agent to version 0.2.0.

## [0.1.2] - 2026-03-27

### Added
- Card creation support via `token`.
- Support for `metadata` in card creation and updates.
- New fields in `CardResponse`: `first_six_digits`, `type`, `label`.

### Changed
- Refined card creation request validation (either `token` or raw card data).
- Updated User-Agent to version 0.1.2.

## [0.1.0] - 2026-03-26

### Added
- Initial release of the Pagar.me Python SDK.
- Core client with asynchronous support using `httpx`.
- Customer management (CRUD and Card sub-resource).
- Order and Charge management.
- Multi-payment method support (Credit Card, Boleto, Pix).
- Pydantic v2 models for all resources.
- Support for full phone parsing.
