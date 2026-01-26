# Performance Budgets

Last updated: 2026-01-24

Scope: Defines latency targets for TestKit and validator operations, and how they are measured and enforced. This doc is about budgets and measurement, not about implementation details of each subsystem.

## If you only read one thing
- These budgets exist to prevent scope creep and keep the tool usable at medium workspace scale.
- Any new feature that makes a budget harder must come with a measurement plan and a mitigation plan.
- "Medium workspace" must be defined by named goldens, not by vibes.

## Update log
- 2026-01-24: Split out from the TestKit v3.6 execution order DOCX (dated 2026-01-21) and converted to Markdown.

## Budgets

| Operation | Target latency |
|---|---|
| Interactive validation (schema + semantic) | < 200ms for medium workspace |
| Full validation (schema + semantic + policy) | < 2s for medium workspace |
| Incremental single-file revalidation | < 100ms |
| Index generation | < 500ms for medium workspace |
| Changeset apply | < 100ms |
