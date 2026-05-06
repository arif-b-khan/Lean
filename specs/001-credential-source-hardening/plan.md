# Implementation Plan: Credential Source Hardening

**Branch**: `001-new-specification` | **Date**: 2026-05-06 | **Spec**: `/specs/001-credential-source-hardening/spec.md`
**Input**: Feature specification from `/specs/001-credential-source-hardening/spec.md`

## Summary

Remove tracked credentials from runtime configuration and load required secrets through .NET user secrets for local development. Enforce startup fail-fast validation against a canonical required-credentials manifest so missing secrets are surfaced immediately with clear setup guidance.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: C# (.NET, Lean solution projects)  
**Primary Dependencies**: Lean configuration system (`Configuration/Config.cs`), .NET user secrets configuration provider  
**Storage**: JSON config files + local developer user secrets store  
**Testing**: `dotnet test` for `Tests/QuantConnect.Tests.csproj` with targeted config/launcher tests  
**Target Platform**: macOS/Linux/Windows local development for Lean Launcher
**Project Type**: Multi-project .NET application  
**Performance Goals**: No measurable startup regression; only lightweight key presence checks at boot  
**Constraints**: No secret fallback to tracked config, fail fast if required secrets are missing, no secret values in logs  
**Scale/Scope**: Launcher startup/config path, tracked runtime config files, secret safety checks in tests/CI

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Determinism: PASS. Behavior is deterministic; startup either validates required secrets or fails with explicit errors.
- Compatibility: PASS with explicit local setup migration note. Breaking local behavior is intentional (no fallback).
- Testing: PASS. Add tests for missing-secret failure modes and successful secret loading.
- Performance: PASS. Validation is bounded by required key count and occurs once at startup.
- Observability: PASS. Errors identify missing key names only; no secret values logged.
- Secret Hygiene: PASS. Credentials removed from tracked runtime config and sourced from user secrets/CI secrets.

## Project Structure

### Documentation (this feature)

```text
specs/001-credential-source-hardening/
├── plan.md
├── spec.md
├── checklists/
│   └── requirements.md
├── required-credentials.json
└── tasks.md
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
Launcher/
├── config.json

Configuration/
└── Config.cs

Tests/
├── Common/
├── Configuration/
└── QuantConnect.Tests.csproj

.github/
└── workflows/

specs/001-credential-source-hardening/
└── required-credentials.json
```

**Structure Decision**: Implement in existing Lean multi-project layout, centered on Launcher config and Configuration pipeline, with tests in existing `Tests/` project and feature docs under `specs/001-credential-source-hardening/`.

## Complexity Tracking

No constitution violations identified.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
