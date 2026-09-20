# Validation — 4.7.5.91

Date: 2026-09-21. Baseline: `d02c4780401218902ef4c0f8d039cfd2f54f1129`.

## Confirmed

- Existing macOS extension matched the upstream repository files byte-for-byte, excluding Chrome-generated `_metadata` and Git metadata.
- The native host requested in `global.min.js` is `2bua8c4s2c.com.agilebits.1password`.
- Read-only check of the existing macOS Chrome host passed: correct name/type, helper file present, expected extension origin already allowed. No host configuration change was needed.
- Seven Python tests passed: public-key ID derivation, read-only behavior, backup/preservation/idempotence, wrong host, missing helper, invalid ID and invalid allowlist.
- Two Node.js tests passed: hidden/disabled field recovery without duplicate icons; accurate inline-click response and sender-tab forwarding.
- JavaScript syntax checks passed.

## Not established by these checks

- A new end-to-end fill with the updated extension and a real vault.
- Compatibility with every login website, two-step flow or future browser release.
- Windows, Linux or browsers other than macOS Chrome.

## Manual acceptance

After loading/reloading the updated extension, unlock the desktop app, test toolbar fill on a trusted login page, and test a hidden login field that becomes visible and is focused. Check the extension service worker for errors. Use a disposable test login and never include its credentials in reports.
