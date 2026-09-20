# 1Password 7 for Chrome — Community Edition

**Keep using your existing 1Password 7 desktop app with a Manifest V3 Chrome extension.**

[简体中文](README.zh-CN.md) · [What changed](CHANGELOG.md) · [Download ZIP](https://github.com/PM100Fun/1password7-chrome-extension/archive/refs/heads/master.zip)

A community-maintained fork of [ferreirafabio/1password7-chrome-extension](https://github.com/ferreirafabio/1password7-chrome-extension), focused on reproducible macOS setup and small, tested usability fixes. This is an unofficial compatibility project, not a 1Password product.

## Why this fork?

The extension code in our existing macOS installation matched upstream. The working native-host configuration did **not** match the host name described in its README. This fork turns that setup knowledge into a repeatable check/repair tool and documents exactly what is inherited and what we changed.

| Inherited from upstream | Added in this fork, 4.7.5.91 |
| --- | --- |
| Manifest V3 service worker compatibility | Correct native-host setup matching the shipped code |
| Native messaging to the desktop app | Read-only configuration check; explicit repair with backup |
| Toolbar, context menu and inline field icons | Hidden/disabled fields remain eligible for icons when focused later |
| Existing Go & Fill / two-step login logic | Accurate inline-click response when no toolbar handler is available |
| Original public manifest key / stable extension ID | English/Chinese instructions and regression tests |

No subscription conversion, vault migration or new extension permissions are introduced by this fork. We do not promise permanent compatibility with future browser or desktop-app versions.

## Quick start — macOS + Google Chrome

You need an installed, licensed 1Password 7 desktop app with browser integration available. Python 3 is needed only for the optional setup tool. Node.js is needed only for development tests.

1. Download and extract the ZIP above, or clone:

   ```sh
   git clone https://github.com/PM100Fun/1password7-chrome-extension.git
   cd 1password7-chrome-extension
   ```

2. Keep the folder in a permanent location. In `chrome://extensions`, enable **Developer mode**, choose **Load unpacked**, and select the folder containing `manifest.json`.
3. Check that the extension ID is `aomjjhallfgjeglblehebfpbcfeobpgk`. This comes from the public `key` in the manifest; it is not a password or private key. If Chrome shows a different ID, use that actual ID with `--extension-id` below.
4. Run the configuration check from the extracted/cloned folder:

   ```sh
   python3 scripts/configure_native_host.py
   ```

   If it reports `MISSING`, repair the existing allowlist:

   ```sh
   python3 scripts/configure_native_host.py --apply
   ```

   The tool validates the host name, helper path and allowlist, preserves other fields and entries, and creates a timestamped backup beside the JSON before replacing it. It does not read your vault or create a missing native host. A missing helper/host must be resolved through the desktop app installation first.

5. Fully quit and reopen Chrome. Open and unlock 1Password 7, then try the toolbar button on a normal HTTPS login page.

### Manual configuration

The **shipped `global.min.js` actually requests**:

```text
2bua8c4s2c.com.agilebits.1password
```

For Google Chrome on macOS, inspect:

```text
~/Library/Application Support/Google/Chrome/NativeMessagingHosts/2bua8c4s2c.com.agilebits.1password.json
```

Back up the existing file and add this entry to its `allowed_origins` array, preserving existing entries and the installed helper path:

```text
chrome-extension://aomjjhallfgjeglblehebfpbcfeobpgk/
```

Editing only `com.1password.1password7.json` does not configure the host requested by this build. Do not replace a working helper path with a guessed SLS helper path.

For a different existing host-file location or unpacked ID:

```sh
python3 scripts/configure_native_host.py --host-file '/absolute/path/to/2bua8c4s2c.com.agilebits.1password.json' --extension-id YOUR_ACTUAL_EXTENSION_ID
```

Add `--apply` only after checking the result. To undo an applied repair, restore the backup file reported by the tool and fully restart Chrome. The tool's exit codes are `0` for OK/updated, `1` for missing allowlist entry and `2` for invalid/missing configuration.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Native messaging host not found | Check the exact host filename above and the helper executable in its `path` field. |
| Access to native messaging host is forbidden | Add the actual extension ID to that host's `allowed_origins`, then fully restart Chrome. |
| Toolbar does nothing | Start/unlock 1Password 7; inspect the extension service worker error; check desktop browser integration. |
| Hidden login field has no icon | Focus the field after it becomes visible; this version retries icon creation. |
| Extension cannot run on `chrome://` pages | Test on an ordinary HTTP/HTTPS page instead. |
| A two-step login fails | Use the toolbar again on the password step; upstream's automatic popup/fill behavior is retained and site-dependent. |

## Compatibility and verification

- The pre-existing macOS installation was reported working by the maintainer; its extension files were compared byte-for-byte with upstream before these changes.
- The local Chrome host name, existing allowlist and helper-file presence were checked with the new tool.
- Configuration safety and JavaScript behavior have automated regression tests. See [validation notes](docs/VALIDATION.md).
- End-to-end credential filling of this updated version is **not yet revalidated**. Automated tests do not prove all websites work.
- Windows, Linux and other Chromium browsers are **not validated** by this fork. The setup tool defaults to macOS Chrome; passing a different file does not establish platform compatibility.
- The extension receives credentials from the desktop app for filling. Broad HTTP/HTTPS access is inherited for this purpose. No telemetry or external service was added by this fork.

## Development

No build step or package installation is needed for the extension. Run checks with Python 3 and Node.js 18+:

```sh
python3 -m unittest discover -s tests -v
node --test tests/extension.test.cjs
node --check background.js
node --check inline-icon.js
```

Reports and contributions are welcome. Include OS, Chrome/1Password versions, steps and a redacted error message. Never include passwords, vault exports or unredacted credential data. If this fork helps you keep an existing setup working, a star helps others discover it.

## Credits and licensing

- Original extension and assets: **AgileBits / 1Password**.
- Manifest V3 port, inline icons and existing compatibility work: **[ferreirafabio](https://github.com/ferreirafabio/1password7-chrome-extension)** and the upstream history.
- Configuration tooling, fixes and bilingual documentation in this fork: **PM100Fun**.

The community-authored code and modifications are under [GPL-3.0](LICENSE), retaining the upstream license. As noted by upstream, `global.min.js`, `injected.min.js`, locales and assets originate from AgileBits and retain their original ownership; this fork does not relicense those materials. Other third-party notices, including those in `ext/sjcl.js`, remain intact. 1Password trademarks belong to their owners. This project is not affiliated with or endorsed by 1Password.
