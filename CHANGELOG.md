# Changelog

## 4.7.5.91 — Community Edition 1 — 2026-09-21

Based on upstream commit `d02c4780401218902ef4c0f8d039cfd2f54f1129`.

### Fixed

- Setup documentation now names the native host actually used by the shipped background bundle: `2bua8c4s2c.com.agilebits.1password`.
- Hidden, disabled and read-only fields are not marked processed before an icon can be created. Focusing an eligible field retries icon creation.
- Inline icon click responses report whether a toolbar handler was available.

### Added

- Read-only macOS Chrome host check and explicit `--apply` repair, with backups, preservation of existing entries and helper-path validation.
- Python configuration tests and Node.js behavior regression tests.
- English and Simplified Chinese setup instructions, troubleshooting, attribution and verification boundaries.

### Unchanged

- Original public manifest key and resulting extension ID.
- Extension permissions, native host selection, bundled vendor code, cryptography and upstream Go & Fill behavior.

## Upstream baseline — 4.7.5.90

Manifest V3 port, native messaging integration, toolbar/context-menu actions and inline icons by upstream. The maintainer's pre-existing macOS extension files matched this baseline; the working host configuration is machine-local and was not an unpublished source-code patch.
