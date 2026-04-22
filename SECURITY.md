## Supported Versions

- Templates generated from the latest `master` commit are supported.
- Older yearly/monthly templates are static snapshots and are not updated once published.

## Ecosystem & Compatibility

| Component         | Version(s) / Tooling               | Notes                                                                       |
| ----------------- | ---------------------------------- | --------------------------------------------------------------------------- |
| OS baseline       | WSL (Ubuntu 25.10)                 | Shared environment across tracks.                                           |
| Ruby generators   | Ruby 4.0.3 (`.ruby-version`)       | Uses Ruby stdlib; add gems per script if needed.                            |
| Python generators | CPython 3.14.4 (`.python-version`) | Uses Python stdlib; add `requirements.txt` if introducing third-party libs. |

## Backward Compatibility

- Generated template formats stay consistent within a calendar year. If we alter a file structure or naming convention, the change log will highlight required migrations.
- Scripts rely on Ruby 4.0.x / Python 3.14.x; earlier interpreter versions are unsupported and will not get fixes.

## Reporting a Vulnerability

Please report issues privately via **GitHub Security Advisory** (preferred) — open through the repository’s **Security → Report a vulnerability** workflow.

Acknowledgement occurs and status updates follow as soon as possible.  
After remediation we publish guidance alongside required dependency updates.
