# Tasks: Credential Source Hardening

**Input**: Design documents from `/specs/001-credential-source-hardening/`
**Prerequisites**: plan.md (required), spec.md (required)

## Phase 1: Setup

- [x] T001 Remove leaked credential from `Launcher/config.json`
- [x] T002 Create canonical required-credentials manifest at `specs/001-credential-source-hardening/required-credentials.json`
- [x] T003 Scan repository for tracked runtime config credential locations and capture findings in `specs/001-credential-source-hardening/research.md`

## Phase 2: Foundational

- [x] T004 Remove credential keys from repository-tracked runtime config files (starting with `Launcher/config.json`)
- [x] T005 Implement user-secrets-aware configuration loading in `Configuration/Config.cs` and launcher startup path
- [x] T006 Add fail-fast startup validation using `specs/001-credential-source-hardening/required-credentials.json`
- [x] T007 Ensure diagnostics/logging never emit secret values (sanitize error paths)

## Phase 3: Validation

- [x] T008 Add automated tests for successful secret loading and missing-secret fail-fast behavior in `Tests/`
- [ ] T009 Add regression test coverage ensuring no secret values are emitted to logs

## Phase 4: Integration & Docs

- [ ] T010 Add CI secret scanning workflow in `.github/workflows/`
- [ ] T011 Update contributor documentation for `dotnet user-secrets` setup and required credentials

## Dependencies & Order

1. Complete T002 and T003 before T005/T006.
2. Complete T005 before T006.
3. Complete T006 and T007 before test tasks T008/T009.
4. Complete implementation and tests before CI/docs updates.
