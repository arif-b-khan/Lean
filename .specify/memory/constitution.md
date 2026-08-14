<!--
Sync Impact Report
- Version change: 1.0.0 -> 1.1.0
- Modified principles:
	- V. Observability and Safe Operations -> V. Observability and Safe Operations
- Added principles:
	- VI. Secret and Credential Hygiene
- Added sections:
	- None
- Removed sections:
	- None
- Templates requiring updates:
	- ✅ updated: .specify/templates/plan-template.md
	- ✅ updated: .specify/templates/tasks-template.md
	- ✅ reviewed, no change needed: .specify/templates/spec-template.md
	- ✅ reviewed, no change needed: .specify/templates/checklist-template.md
	- ✅ reviewed: .specify/templates/commands/*.md (directory not present)
- Follow-up TODOs:
	- None
-->

# Lean Constitution

## Core Principles

### I. Deterministic Engine Behavior
All engine and model changes MUST preserve deterministic behavior for identical inputs,
configuration, and data. Any intentional behavior change MUST be explicitly documented in
the feature spec and validated by tests that distinguish old and new behavior.
Rationale: deterministic outcomes are required for trustworthy backtesting,
reproducibility, and regression analysis.

### II. Backward-Compatible Public Contracts
Public contracts (algorithm APIs, brokerage/data interfaces, file formats, and CLI/runtime
surfaces) MUST remain backward compatible unless a breaking change is approved through an
explicit migration plan. Breaking changes MUST include deprecation notes, versioned
transition guidance, and release-note impact statements.
Rationale: LEAN is an ecosystem platform with external users, integrations, and strategies
that depend on contract stability.

### III. Test-Backed Changes (NON-NEGOTIABLE)
Every production code change MUST include or update automated tests at the appropriate
level (unit, integration, or regression). Changes that alter observable behavior MUST add
regression coverage. A change MUST NOT be considered complete unless the required tests are
passing locally or in CI.
Rationale: automated validation is the primary defense against subtle strategy, data, and
execution regressions.

### IV. Performance and Resource Discipline
Code in hot paths (data feed handling, indicator updates, order processing, and
backtest/live loops) MUST be evaluated for runtime and memory impact. Features that increase
complexity MUST justify the tradeoff and include mitigation (profiling evidence,
short-circuit paths, batching, or caching strategy as applicable).
Rationale: performance and predictable resource usage are core product requirements for
backtesting scale and live-trading reliability.

### V. Observability and Safe Operations
Operationally significant paths MUST emit actionable diagnostics (errors, warnings, and
context needed for triage) without leaking secrets or sensitive credentials. Failure modes
MUST degrade safely, returning clear errors over silent corruption or undefined behavior.
Rationale: high-confidence incident response requires useful telemetry and secure handling
of operational data.

### VI. Secret and Credential Hygiene
Credentials, API keys, tokens, certificates, and other confidential material MUST NOT be
committed to source code, repository-tracked configuration, examples, tests, or logs. Any
required secret MUST be injected through secure runtime mechanisms (environment variables,
secret managers, or CI secret stores) and excluded from version control.
Rationale: leaked credentials in a public repository create immediate security risk and
potential compromise of user, infrastructure, and brokerage resources.

## Engineering Constraints

- Core runtime and engine changes MUST preserve existing architecture conventions used in
  this repository (C#/.NET solution structure, Python interoperability boundaries, and
  existing extension points).
- Feature specs MUST state compatibility impact, target components, and test strategy before
  implementation planning is finalized.
- Pull requests MUST scope changes to the minimum necessary surface area and avoid unrelated
  refactors unless separately justified.
- Configuration changes MUST provide safe defaults and explicit documentation for new options.
- Repository-tracked configuration MUST use placeholders for sensitive values and MUST document
	secure secret injection paths instead of hardcoded credentials.

## Development Workflow and Quality Gates

1. Specifications created with Spec Kit MUST define independently testable user stories and
	explicit acceptance criteria.
2. Implementation plans MUST pass the Constitution Check by mapping each principle to
	concrete verification tasks.
3. Task lists MUST include required automated testing tasks for each story that changes
	production behavior.
4. Code review MUST verify determinism impact, compatibility impact, test adequacy,
	performance risk, observability implications, and credential-handling safety.
5. CI/build failures on required checks MUST block merge until resolved.

## Governance

This constitution is the authoritative engineering policy for planning and implementing
changes in this repository. In case of conflict, this document takes precedence over ad hoc
workflow preferences.

Amendment process:
1. Propose changes in a dedicated pull request that explains rationale, expected impact,
	and migration or rollout guidance when behavior changes.
2. Obtain maintainer approval from repository owners.
3. Update dependent templates and workflow guidance in the same change.

Versioning policy for this constitution uses semantic versioning:
1. MAJOR: incompatible governance or principle removals/redefinitions.
2. MINOR: new principle/section or materially expanded requirement.
3. PATCH: clarifications, wording improvements, and non-semantic edits.

Compliance review expectations:
1. Every feature plan and implementation review MUST include a constitution compliance check.
2. Violations MUST be documented with explicit justification and follow-up remediation tasks.
3. Periodic governance review SHOULD occur at least once per quarter or when major workflow
	changes are introduced.

**Version**: 1.1.0 | **Ratified**: 2026-05-06 | **Last Amended**: 2026-05-06
