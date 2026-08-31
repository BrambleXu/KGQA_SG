# Security

This repository is a local educational demo, not a hardened public service. The development server binds to loopback and disables the debugger. Do not expose it directly to the Internet or commit database credentials.

Only the current Python 3.14 / uv-based code is maintained. The 2018 dependency set is unsupported.

## Verification

Run the checks in [README.md](README.md#开发与安全检查). Both Python and npm audits must pass, and the vendored browser assets must match the locked packages. A skipped or failed dependency lookup is a failed audit; there is no advisory allowlist. A clean scan only means no known vulnerability was reported by the databases at that time.

For dependency updates, commit regenerated requirements and browser assets with the lockfiles. Never dismiss an alert solely to make the alert count zero.

The [2026-08-31 remediation record](docs/security/remediation-2026-08-31.md) documents the original 62 GitHub alerts and the local fixes. GitHub closes dependency alerts only after it evaluates the updated default branch; local test results are not proof of remote closure.

## Reporting

For a suspected vulnerability, record the affected commit, package/version, impact and a minimal reproduction. Do not post credentials, personal data, or weaponized exploit payloads in public issues. Check the repository's Security tab for an available private reporting route before disclosing sensitive details. This document does not promise that private reporting is enabled.

The historical graph and biographies are not verified historical or biographical reference data.
