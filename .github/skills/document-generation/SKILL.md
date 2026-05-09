---
name: document-generation
description: "Generate and maintain Lean feature documentation with MkDocs. Use for creating feature docs, organizing docs under Docs/generated, keeping MkDocs navigation updated, and ensuring browser preview and build validation. Triggers: generate docs, write feature document, docs workflow, mkdocs docs, documentation standard."
argument-hint: "Feature name and what changed"
---

# Document Generation Workflow

## Outcome

Produce a feature documentation page that:

- Is stored in the required project folder structure
- Is linked in MkDocs navigation
- Can be previewed locally in a browser
- Includes implementation and validation details

## When To Use

Use this workflow when:

- A new feature is implemented and needs technical documentation
- Existing behavior changes require doc updates
- You need consistent generated docs in this repository

## Inputs

- Feature name in kebab-case (example: workflow-fix)
- Brief summary of behavior or API changes
- Validation commands or test evidence

## Procedure

1. Confirm framework and location constraints

- Use MkDocs as the required framework.
- Store generated docs only under Docs/generated.

2. Create feature folder structure

- Create Docs/generated/<feature-name>/index.md.
- Create Docs/generated/<feature-name>/assets/ for diagrams and images.

3. Author the feature document

- Include these sections:
    1. Purpose and scope
    2. Design summary
    3. Public API or behavior changes
    4. Configuration and usage
    5. Validation steps (build/test)
    6. Risks, limitations, rollback notes

4. Ensure MkDocs site integration

- Confirm mkdocs.yml exists.
- Add navigation entry for the new feature page.
- Ensure Docs/generated/index.md references generated docs conventions.

5. Validate browser run

- Run local preview: mkdocs serve -a 127.0.0.1:8000.
- Confirm page opens in browser and navigation works.
- Run static build validation: mkdocs build.

6. Apply change discipline

- Keep docs changes focused on the same feature.
- Update docs in the same change as behavior updates.
- Link to existing docs instead of duplicating content.

## Decision Points

- If MkDocs is not installed:
    - Install mkdocs first.
    - Optional: install mkdocs-material.
- If a proposed doc path is outside Docs/generated:
    - Move it into Docs/generated/<feature-name>/index.md.
- If behavior changed but docs were not updated:
    - Add or amend the feature document before completion.

## Completion Checks

- Feature page exists at Docs/generated/<feature-name>/index.md.
- Assets are under Docs/generated/<feature-name>/assets/.
- mkdocs.yml includes or can resolve navigation to the new page.
- mkdocs serve runs and page is reachable in browser.
- mkdocs build completes successfully.

## Related Project Standards

- Lean engineering standards are described in .github/instructions/lean-engineering-principles.instructions.md.
- Documentation principles are described in .github/instructions/document-generation-principles.instructions.md.
