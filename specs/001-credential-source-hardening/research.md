# Credential Location Scan

Date: 2026-05-06

## Scope

- `Launcher/config.json`
- Repository-tracked runtime and example config files

## Findings

- Removed leaked secret from `Launcher/config.json` (`ib-password`).
- Removed credential key entries from `Launcher/config.json` and moved secret resolution to runtime user-secrets loading.
- Removed `api-access-token` from `DownloaderDataProvider/config.example.json`.
- No additional tracked runtime config files with confirmed literal credential values were identified in this pass.

## Sensitive Key Classes Identified

- Token fields: `*-token`, `*auth-token`, `*refresh-token`
- Password fields: `*-password`
- Secret fields: `*-secret`
- API key fields: `*-api-key`, `*app-key`
- Private key fields: `*private-key*`

## Next Implementation Steps

1. Remove credential key entries from tracked runtime config files where policy requires key removal.
2. Load these values from `.NET user-secrets` at runtime.
3. Fail fast at startup for missing required keys using `required-credentials.json`.
4. Add regression tests and CI secret scanning.
