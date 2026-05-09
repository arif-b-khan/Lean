---
description: "Use when creating, updating, or organizing technical documentation for Lean features. Enforces document location, structure, and browser preview workflow using MkDocs."
applyTo: ["Docs/**", "**/*.md", "mkdocs.yml"]
---

# Document Generation Principles

## Required Framework

- Use MkDocs as the required documentation framework for this repository.
- Material theme is optional. If `mkdocs-material` is installed, it may be enabled for improved UX.
- Keep documentation sources in Markdown.

## Storage and Naming Rules

- Store all agent-generated feature documentation under `Docs/generated/`.
- For each feature, create a folder using kebab-case:
    - `Docs/generated/<feature-name>/index.md`
- Place images and diagrams under:
    - `Docs/generated/<feature-name>/assets/`
- Do not place generated feature docs in root folders such as `Algorithm/`, `Engine/`, or repository root.

## Document Content Standard

Each feature document should include:

1. Purpose and scope
2. Design summary
3. Public API or behavior changes
4. Configuration and usage
5. Validation steps (build/test)
6. Risks, limitations, and rollback notes

## Browser-Run Requirement

- Documentation must be previewable locally in a browser via MkDocs.
- Ensure docs are reachable from MkDocs navigation.
- Standard local preview command:
    - `mkdocs serve -a 127.0.0.1:8000`
- Generated static site command:
    - `mkdocs build`

## Change Discipline

- Keep docs changes focused on the feature being delivered.
- Update docs in the same change as the code when behavior changes.
- Avoid duplicated content; link to existing docs when possible.
