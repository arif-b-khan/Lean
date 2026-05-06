# Feature Specification: Credential Source Hardening

**Feature Branch**: `001-new-specification`  
**Created**: 2026-05-06  
**Status**: Draft  
**Input**: User description: "Remove all the credentials from the config.json file. Add the feature to read the user credentials from dotnet user secrets"

## Clarifications

### Session 2026-05-06

- Q: What credential-source fallback policy should be used when .NET user secrets are unavailable? → A: Only .NET user secrets are valid; if unavailable, startup fails with guidance.
- Q: What file scope should be covered for credential removal? → A: All repository-tracked runtime config files, with Launcher/config.json as mandatory first target.
- Q: When should required secret keys be validated? → A: Validate all required secret keys at startup and fail immediately if any are missing or invalid.
- Q: How should tracked runtime config represent credentials after migration? → A: Remove credential keys entirely from tracked runtime config files.
 - Q: Where should the canonical required credential keys be declared? → A: In a single manifest `specs/001-credential-source-hardening/required-credentials.json` used by startup validation and contributor docs.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Remove Repository Credentials (Priority: P1)

As a maintainer of this public repository, I need all credentials removed from repository-tracked configuration so no confidential values are exposed in source control.

**Why this priority**: This directly addresses immediate security risk and repository hygiene requirements.

**Independent Test**: Can be fully tested by inspecting repository-tracked runtime configuration files and confirming credential keys/values are absent, with no real secret values committed.

**Acceptance Scenarios**:

1. **Given** repository-tracked configuration contains credential values, **When** the feature is applied, **Then** credential keys and values are removed from repository-tracked runtime config files.
2. **Given** a contributor clones the repository, **When** they inspect tracked configuration, **Then** they cannot obtain usable credentials from any tracked file.

---

### User Story 2 - Load Credentials From User Secrets (Priority: P1)

As a local developer, I need runtime credential resolution from a local secret store so I can run the application without storing secrets in tracked files.

**Why this priority**: The secure replacement path must exist for local functionality after removing credentials from tracked config.

**Independent Test**: Can be fully tested by providing credentials only via local user secrets and verifying the application authenticates successfully without credentials present in tracked configuration.

**Acceptance Scenarios**:

1. **Given** tracked configuration does not contain credentials and valid local user secrets are configured, **When** the application starts, **Then** credential-dependent functionality works using locally stored secrets.
2. **Given** tracked configuration does not contain credentials and local user secrets are missing, **When** the application starts, **Then** the application fails safely with clear guidance on how to provide required secrets.

---

### User Story 3 - Preserve Non-Secret Configuration Behavior (Priority: P2)

As a developer, I need non-secret configuration behavior to remain unchanged so existing local workflows continue to work after secret source migration.

**Why this priority**: Ensures security improvements do not regress unrelated configuration behavior.

**Independent Test**: Can be fully tested by running existing startup/configuration flows and verifying non-secret settings behave the same as before.

**Acceptance Scenarios**:

1. **Given** existing non-secret configuration settings, **When** the application reads configuration after this feature, **Then** non-secret values are loaded and applied exactly as before.

### Edge Cases

- What happens when user secrets contain only a subset of required credential keys?
- How does the system handle malformed or empty secret values in local secret storage?
- What happens when legacy credential values are still present in a tracked config file after migration?
- How does the system behave in environments where local user secrets are unavailable?
- How does the system fail when environment variables are present but .NET user secrets are missing?
- How are credentials handled when discovered in repository-tracked runtime config files outside Launcher/?
- How are invalid secret values reported when startup validation fails?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST remove all credential keys and values from all repository-tracked runtime configuration files, with Launcher/config.json treated as the mandatory first target.
- **FR-002**: The system MUST support reading required user credentials from local .NET user secrets at runtime.
- **FR-003**: The system MUST prioritize local .NET user-secret values over any credential values found in repository-tracked runtime configuration.
- **FR-004**: The system MUST provide a clear, actionable error message when required credentials are missing from local secret storage.
- **FR-004a**: The system MUST treat .NET user secrets as the only valid credential source for this feature and MUST NOT use environment variables or repository-tracked configuration values as credential fallbacks.
- **FR-004b**: The system MUST validate all required credential keys during startup and MUST fail fast before runtime operations when any required key is missing or invalid.
- **FR-005**: The system MUST keep non-secret configuration behavior unchanged relative to current behavior.
- **FR-006**: The system MUST document the required secret keys and the local setup workflow for contributors.
 - **FR-006**: The system MUST document the required secret keys and the local setup workflow for contributors. The required keys MUST be listed in `specs/001-credential-source-hardening/required-credentials.json`, which is the canonical manifest consumed by startup validation and documentation.
- **FR-007**: The system MUST ensure logs and diagnostics do not print full credential values.

### Key Entities *(include if feature involves data)*

- **Credential Key**: A named credential input required for runtime authentication (for example username, password, token, or API key).
- **Secret Source**: The local secure configuration source that stores credential keys and values outside repository-tracked files.
- **Runtime Configuration Profile**: The complete set of configuration inputs used at startup, combining non-secret tracked settings and secret values resolved at runtime.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of repository-tracked runtime configuration files contain zero credential keys and zero real credential values after migration.
- **SC-002**: In local developer validation, 95% or more startup attempts with correctly configured local secrets complete without credential-related errors.
- **SC-003**: 100% of startup attempts without required credentials fail with an actionable message that identifies missing keys and setup steps.
- **SC-004**: At least 90% of contributors executing the documented setup can configure local secrets and run the launcher in under 10 minutes.

## Assumptions

- Contributors running this feature locally have permission to create and use local user secrets on their machines.
- This feature is limited to local credential loading and does not introduce new remote secret-management dependencies.
- Existing non-secret configuration keys and default behavior remain valid and should not be redesigned in this feature.
- Secret key names and credential requirements can be documented without exposing actual secret values.
- Environments without support for .NET user secrets are out of scope for credentialed startup in this feature and are expected to fail with setup guidance.
