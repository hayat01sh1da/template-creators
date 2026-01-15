# Security Policy

## Supported Versions

- Templates generated from the latest `master` commit are supported.
- Older yearly/monthly templates are static snapshots and are not updated once published.

## Ecosystem & Compatibility

| Component            | Version(s) / Tooling            | Notes |
| -------------------- | ------------------------------ | ----- |
| OS baseline          | WSL (Ubuntu 24.04.3 LTS)       | Matches the README instructions. |
| Ruby generators      | Ruby 4.0.1 (`.ruby-version`)   | Uses Ruby stdlib; add gems per script if needed. |
| Python generators    | CPython 3.14.2 (`.python-version`) | Uses Python stdlib; add `requirements.txt` if introducing third-party libs. |

## Backward Compatibility

- Generated template formats stay consistent within a calendar year. If we alter a file structure or naming convention, the change log will highlight required migrations.
- Scripts rely on Ruby 4.0.x / Python 3.14.x; earlier interpreter versions are unsupported and will not get fixes.

## Reporting a Vulnerability

Report issues privately through GitHub’s **Security → Report a vulnerability** workflow or by emailing `security@project.org` with reproduction steps (e.g.,
input prompts, generated filenames). Expect acknowledgement within **3 business days** and updates at least every **7 business days**.
