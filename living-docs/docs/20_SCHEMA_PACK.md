# Schema Pack Canon (PTBL v2.6.19)

Last updated: 2026-01-24

Scope: Canonical, implementation-facing reference for the PTBL v2.6.19 schema pack (10 JSON Schemas plus the lint and meta-test scripts). This is written to be a reliable navigation aid for humans and LLM agents working inside `ptbl-testkit`.

## If you only read one thing, read this section
- Treat each schema's **`$id` as the contract**, not the filename. Filenames can change; `$id` must stay stable for resolver correctness.
- `ptbl-base-v2_6_19_min.json` is the shared primitives library. Everything else builds on its `$defs` (StableUID, typed refs, Duration, CronExpression, ConfigBag).
- PTBL separates **authored manifests** from **derived artifacts** (index, changeset, lock). Do not mix these layers in tooling or in validation expectations.
- Identity must be unambiguous: use StableUID as the single identity, avoid duplicate `uid` fields, and validate typed refs instead of stringly references.
- Keep determinism: derived artifacts, diagnostics, and reports must be byte-for-byte stable when inputs are unchanged.

## Update log
- 2026-01-24: Converted `PTBL_Core_Schema_Documentation_v2_6_19.docx` into this living Markdown canon and aligned terminology for TestKit usage.

## 1. What this documentation is for

The PTBL core schemas are a coordinated set. They model application intent, reusable modules, infra intent and plans, data pipelines, integrations, security, deployment, and the derived artifacts used for deterministic builds (lockfiles, indexes, changesets). Because these files evolve together, documentation must explain both each file and the system-level contracts across files.

This document is designed to work as a single source of truth. If you later want a Notion or Confluence structure, each section can be copied into a page with minimal editing.

## 2. Mental model: four artifact layers

- **Layer 0**: Shared primitives
  - ptbl-base (types, identity rules, workflow and agent building blocks)
- **Layer 1**: Authored manifests (source of truth)
  - ptbl-module (reusable modules)
  - ptbl-app-* (application manifests split by concern: core, data, integrations, security, deployment)
- **Layer 2**: Change and workspace operations
  - ptbl-changeset (planned edits and patch operations)
  - ptbl-index (workspace index for editors and impact analysis)
- **Layer 3**: Deterministic resolution outputs
  - ptbl-lock (exact resolved dependency references and integrity hashes)

Key principle: authored manifests describe intent. Derived artifacts describe resolution results, indexing, and edits. These are kept separate so builds remain reproducible and editors remain safe.

## 3. Package inventory

| Item | Details |
| --- | --- |
| CHANGELOG-v2_6_19.md | Release notes and validation status for v2.6.19. |
| ptbl-app-core-v2_6_19_min.json | JSON Schema, draft 2020-12. $id: https://prompt.build/ptbl/2.6.19/app-core |
| ptbl-app-data-v2_6_19_min.json | JSON Schema, draft 2020-12. $id: https://prompt.build/ptbl/2.6.19/app-data |
| ptbl-app-deployment-v2_6_19_min.json | JSON Schema, draft 2020-12. $id: https://prompt.build/ptbl/2.6.19/app-deployment |
| ptbl-app-integrations-v2_6_19_min.json | JSON Schema, draft 2020-12. $id: https://prompt.build/ptbl/2.6.19/app-integrations |
| ptbl-app-security-v2_6_19_min.json | JSON Schema, draft 2020-12. $id: https://prompt.build/ptbl/2.6.19/app-security |
| ptbl-base-v2_6_19_min.json | JSON Schema, draft 2020-12. $id: https://prompt.build/ptbl/2.6.19/base |
| ptbl-changeset-v2_6_19_min.json | JSON Schema, draft 2020-12. $id: https://prompt.build/ptbl/2.6.19/changeset |
| ptbl-index-v2_6_19_min.json | JSON Schema, draft 2020-12. $id: https://prompt.build/ptbl/2.6.19/index |
| ptbl-lock-v2_6_19_min.json | JSON Schema, draft 2020-12. $id: https://prompt.build/ptbl/2.6.19/lock |
| ptbl-module-v2_6_19_min.json | JSON Schema, draft 2020-12. $id: https://prompt.build/ptbl/2.6.19/module |
| ptbl_lint_v2_6_19.py | Python tooling: lint gate, meta tests, regression tests. |
| ptbl_schema_meta_tests.py | Python tooling: lint gate, meta tests, regression tests. |
| ptbl_schema_regression_tests.py | Python tooling: lint gate, meta tests, regression tests. |

## 4. What goes where

Use this as the practical routing guide when deciding which schema file should contain a new concept.

| File | Scope |
| --- | --- |
| ptbl-app-core | App identity, imports, high-level architecture, infra intent and resolved infra plan, UI roots, global settings. |
| ptbl-app-data | Datasets, ETL pipelines, data quality checks, analytical views, batch jobs that are data-centric. |
| ptbl-app-integrations | External systems and adapters, credentials references, webhooks, sync and polling behaviors. |
| ptbl-app-security | Authn/authz, policies, data protection rules, audit configurations, security posture knobs. |
| ptbl-app-deployment | Runtime topology and deployment behaviors, regions, hybrid/on-prem agent requirements. |
| ptbl-module | Reusable modules: entities, APIs, workflows, agents, events, migrations. Intended to be imported. |
| ptbl-lock | Exact resolved module references and integrity hashes. Generated by tooling, not hand-edited. |
| ptbl-index | Workspace index for fast lookups, reverse dependencies, and editor support. Generated by tooling. |
| ptbl-changeset | Structured edit plan: patches, impact, validation and execution results. Authored by editors and agents, enriched by automation. |
| ptbl-base | Shared primitives and building blocks. No app-specific concepts here. |

## 5. Dependency model across schemas

Schemas reference each other using $ref with $id URLs. Filenames are not the contract. This makes refs stable when schemas are hosted in a registry or served from a website. In practice, the dependency direction is intentionally one-way: ptbl-base is the foundation.

### 5.1 Dependency diagram

ptbl-base
  -> ptbl-module
  -> ptbl-app-core
  -> ptbl-app-data
  -> ptbl-app-integrations
  -> ptbl-app-security
  -> ptbl-app-deployment
  -> ptbl-lock
  -> ptbl-index
  -> ptbl-changeset

### 5.2 Dependency matrix with reference counts

| Item | Details |
| --- | --- |
| ptbl-app-core-v2_6_19_min.json | ptbl-base-v2_6_19_min.json (76) |
| ptbl-app-data-v2_6_19_min.json | ptbl-base-v2_6_19_min.json (72) |
| ptbl-app-deployment-v2_6_19_min.json | ptbl-base-v2_6_19_min.json (14) |
| ptbl-app-integrations-v2_6_19_min.json | ptbl-base-v2_6_19_min.json (43) |
| ptbl-app-security-v2_6_19_min.json | ptbl-base-v2_6_19_min.json (68) |
| ptbl-changeset-v2_6_19_min.json | ptbl-base-v2_6_19_min.json (17) |
| ptbl-index-v2_6_19_min.json | ptbl-base-v2_6_19_min.json (44) |
| ptbl-lock-v2_6_19_min.json | ptbl-base-v2_6_19_min.json (6) |
| ptbl-module-v2_6_19_min.json | ptbl-base-v2_6_19_min.json (31) |

### 5.3 Most used base primitives by other schemas

- **ConfigBag**: Refs: 103. Flexible configuration container. The ONLY supported open config surface.

- **StableUID**: Refs: 81. Immutable identifier. Format: {module}_{elementtype}_{name}. All lowercase, underscores only. 3-128 chars. NEVER changes after creation. Map keys for entities/apis/workf…

- **Duration**: Refs: 74. ISO 8601 duration or shorthand. Examples: PT1H (1 hour), P1D (1 day), 30s, 5m, 1h, 24h, 7d.

- **SecretRef**: Refs: 24. Reference to secret/credential/key in secrets management.

- **ConnectionRef**: Refs: 23. Reference to connection configuration.

- **IntegrityHash**: Refs: 12. SHA-256 hash of canonical content (lowercase hex). Canonicalization: parse source (YAML/JSON) -> emit compact JSON with sorted keys -> UTF-8 encode -> SHA-256 -> lowerca…

- **ScheduleExpression**: Refs: 8. Cron expression or preset like @daily, @hourly

- **JsonPointer**: Refs: 7. RFC 6901 JSON Pointer. All map keys in paths MUST be snake_case to match propertyNames constraints.

- **ScopedPatchOperation**: Refs: 3. Patch operation anchored by element uid, making it rename-safe. The json_pointer is relative to the element root.

- **SchemaDefinition**: Refs: 3.

- **OwnerContact**: Refs: 2.

- **ChangelogEntry**: Refs: 2.

- **ADR**: Refs: 2. Architecture Decision Record - captures why decisions were made

- **TestCoverageMapping**: Refs: 2. Maps PTBL specs to test coverage

- **MetadataBag**: Refs: 2. Extension metadata container.

- **CronExpression**: Refs: 2. Cron expression for scheduling. Standard 5-field (minute hour day month weekday) or 6-field with seconds.

- **RetryConfig**: Refs: 2.

- **JsonValue**: Refs: 2. Any valid JSON value. Use sparingly - prefer typed schemas.

- **AppRootUID**: Refs: 1. App root identifier. Format: {appname}_app_root.

- **Entrypoint**: Refs: 1. Application entry point definition

## 6. Core conventions

### 6.1 Identity and rename-safe design

Collections that represent addressable objects use a map keyed by StableUID. The object value does not repeat the uid. This prevents dual identity and supports rename-safe patch operations, since a rename is represented as a map key change, not an in-object field edit.

StableUID rules:

- snake_case only

- prefix conventions: module_entity_name, module_api_name, module_workflow_name, etc

- treat StableUID as immutable once published

### 6.2 Strict schemas and safe extension points

Schemas are designed to be strict. Open objects are not allowed unless explicitly modeled. When extension is needed, use typed bags such as ConfigBag with clear constraints, or introduce a discriminated union with explicit variants.

Preferred extension strategies:

- Discriminated unions with a type field and per-variant required payload

- ConfigBag for engine-specific knobs that are not part of the public semantic contract

- Avoid additionalProperties true on domain objects

### 6.3 Durations and schedules are typed

Duration-like fields must use the Duration type. Schedule-like fields must use CronExpression or ScheduleExpression. This avoids string drift and reduces ambiguity for LLM generation and validators.

## 7. End-to-end workflows

### 7.1 Authoring, validation, and build

1) Author or generate manifests
   - ptbl-module, ptbl-app-*
2) Validate schemas and instances
   - ptbl_lint + schema meta tests + regression tests
3) Resolve imports and pin exact versions
   - produce ptbl-lock
4) Build workspace index for editors and tooling
   - produce ptbl-index
5) Plan and apply structured edits
   - produce and apply ptbl-changesets

### 7.2 Determinism contract

Determinism is achieved by separating intent from resolution and by locking dependencies. Given the same authored manifests and the same lockfile, the build should resolve to the same effective workspace.

## 8. File reference

### ptbl-base-v2_6_19_min.json

- **Title**: PTBL Base Definitions

- **Role**: Schema library

- **Scope**: Shared primitives and building blocks

- **Produced by**: Schema authors

- **Consumed by**: All other schemas and tooling

- **$id**: https://prompt.build/ptbl/2.6.19/base

Shared definitions for PTBL schemas. Referenced by module and app schemas.

#### Dependencies

- **Depends on**: None

- **Depended on by**: ptbl-app-core-v2_6_19_min.json (76), ptbl-app-data-v2_6_19_min.json (72), ptbl-app-security-v2_6_19_min.json (68), ptbl-index-v2_6_19_min.json (44), ptbl-app-integrations-v2_6_19_min.json (43), ptbl-module-v2_6_19_min.json (31), ptbl-changeset-v2_6_19_min.json (17), ptbl-app-deployment-v2_6_19_min.json (14), ptbl-lock-v2_6_19_min.json (6)

#### Top-level structure

This file is a definitions library ($defs) with minimal or no top-level properties.

#### Key definitions

| Definition | Notes |
| --- | --- |
| AgentSpec | Agent specification. Map key IS the StableUID; do not include uid field. |
| EntitySpec | Entity specification. Map key IS the StableUID; do not include uid field. |
| WorkflowStep | Workflow step. Discriminated by 'type' field - each type requires specific fields. |
| StableUID | Immutable identifier. Format: {module}_{elementtype}_{name}. All lowercase, underscores only. 3-128 chars. NEVER changes after creation. Map keys for entities/apis/workflows/etc MUST be StableUIDs. |
| Duration | ISO 8601 duration or shorthand. Examples: PT1H (1 hour), P1D (1 day), 30s, 5m, 1h, 24h, 7d. |
| ConfigBag | Flexible configuration container. The ONLY supported open config surface. |
| SecretRef | Reference to secret/credential/key in secrets management. |
| WorkflowSpec | Workflow specification. Discriminated by 'mode' field. Map key IS the StableUID; do not include uid field. |
| ScheduledJobSpec | ScheduledJob specification. Map key IS the StableUID; do not include uid field. |
| ApiEndpointSpec | ApiEndpoint specification. Map key IS the StableUID; do not include uid field. |
| QueueSpec | Queue specification. Map key IS the StableUID; do not include uid field. |
| EventSpec | Event specification. Map key IS the StableUID; do not include uid field. |
| WorkflowEdge | Explicit edge in graph workflow (optional - can infer from node.next) |
| AgentTool | Tool available to an agent. Discriminated by 'type' field. |
| WorkflowNode | Node in a graph-based workflow (LangGraph-style) |
| AgentOrchestration | Multi-agent orchestration configuration |
| WorkflowTrigger |  |
| WorkflowState |  |

#### Minimal valid skeleton (shape guide)

{}

#### Common pitfalls

- Do not place app-specific concepts here. Keep this a shared primitives library.

- Prefer discriminated unions over loosely typed objects.

### ptbl-app-core-v2_6_19_min.json

- **Title**: PTBL App Core Schema

- **Role**: Authored manifest

- **Scope**: App identity, imports, infra intent and plan, UI roots

- **Produced by**: LLM generator or app authors

- **Consumed by**: Compiler; infra planner; UI tooling

- **$id**: https://prompt.build/ptbl/2.6.19/app-core

Schema for PTBL application manifests. v2.6.19: UI uses registry pattern.

#### Dependencies

- **Depends on**: ptbl-base-v2_6_19_min.json (76)

- **Depended on by**: None

#### Top-level structure

| Key | Required | Type | Meaning |
| --- | --- | --- | --- |
| ptbl | Yes | string | PTBL schema version |
| generated_by | No | object |  |
| app | Yes | object |  |
| imports | Yes | array | Modules that compose this application (at least one required) |
| infra | No | $ref |  |
| observability | No | $ref |  |
| tests | No | $ref |  |
| ui | No | $ref |  |
| docs | No | $ref |  |
| multi_tenancy | No | $ref |  |

#### Key definitions

| Definition | Notes |
| --- | --- |
| UIComponentSpec | UI component specification. Map key IS the UIComponentUID. Do not include id field. |
| WorkflowAction |  |
| InfraPlan | Agent-generated resolved infrastructure plan (what the system will deploy) |
| InfraAutomanage | Automation controls and safety guardrails for agent-managed infrastructure |
| InfraIntent | User-specified infrastructure constraints and goals (what the user wants) |
| MultiTenancyConfig | Multi-tenancy architecture configuration - foundational for SaaS |
| InfraPlanService | Resolved configuration for a single service |
| UIConfig |  |
| UIComponent |  |
| UIAction |  |
| ThemeConfig |  |
| ScalingConfig |  |
| ResourceConfig |  |
| PageConfig |  |
| ObservabilityConfig |  |
| NavigateAction |  |
| ModalAction |  |
| LayoutConfig |  |

#### Minimal valid skeleton (shape guide)

```json
{
  "ptbl": "<string>",
  "app": {},
  "imports": []
}
```

#### Common pitfalls

- Do not move data pipeline details here. Keep app-core focused on architecture and infra intent.

- Imports should remain the primary mechanism for reuse. Avoid duplicating module content into apps.

### ptbl-app-data-v2_6_19_min.json

- **Title**: PTBL App Data Schema

- **Role**: Authored manifest

- **Scope**: Datasets, ETL pipelines, data operations

- **Produced by**: LLM generator or app authors

- **Consumed by**: ETL engine; analytics; scheduler

- **$id**: https://prompt.build/ptbl/2.6.19/app-data

Data platform, analytics, ML, ETL

#### Dependencies

- **Depends on**: ptbl-base-v2_6_19_min.json (72)

- **Depended on by**: None

#### Top-level structure

| Key | Required | Type | Meaning |
| --- | --- | --- | --- |
| storage | No | $ref |  |
| cache | No | $ref |  |
| search | No | $ref |  |
| analytics | No | $ref |  |
| bigdata | No | $ref |  |
| ml | No | $ref |  |
| data_lineage | No | $ref |  |

#### Key definitions

| Definition | Notes |
| --- | --- |
| ETLSensor | Sensor that waits for external conditions before proceeding |
| ETLPipeline | ETL/ELT pipeline with DAG support |
| ETLTask | A task/node in an ETL DAG |
| DataQualityCheck | Data quality validation |
| StorageConfig |  |
| SearchConfig |  |
| MLConfig |  |
| DataLineageConfig |  |
| CacheConfig |  |
| BigDataConfig |  |
| AnalyticsConfig |  |

#### Minimal valid skeleton (shape guide)

{}

#### Common pitfalls

- Do not use plain strings for durations or schedules. Use Duration and schedule primitives.

- Avoid mixing integration connection config here. Put that in integrations and reference it.

### ptbl-app-deployment-v2_6_19_min.json

- **Title**: PTBL App Deployment Schema

- **Role**: Authored manifest

- **Scope**: Deployment topology, regions, hybrid/on-prem agents

- **Produced by**: LLM generator or platform authors

- **Consumed by**: Deploy orchestrator; runtime manager

- **$id**: https://prompt.build/ptbl/2.6.19/app-deployment

Deployment topology and on-premises agents

#### Dependencies

- **Depends on**: ptbl-base-v2_6_19_min.json (14)

- **Depended on by**: None

#### Top-level structure

| Key | Required | Type | Meaning |
| --- | --- | --- | --- |
| deployment | Yes | $ref |  |

#### Key definitions

| Definition | Notes |
| --- | --- |
| OnPremAgent | On-premises agent configuration |
| DeploymentConfig | Deployment topology including hybrid and on-premises configurations |
| DeploymentRegion |  |

#### Minimal valid skeleton (shape guide)

```json
{
  "deployment": "<value>"
}
```

### ptbl-app-integrations-v2_6_19_min.json

- **Title**: PTBL App Integrations Schema

- **Role**: Authored manifest

- **Scope**: External system integrations and credentials references

- **Produced by**: LLM generator or app authors

- **Consumed by**: Integration runtime; connectors

- **$id**: https://prompt.build/ptbl/2.6.19/app-integrations

External integrations, payments, notifications, and features

#### Dependencies

- **Depends on**: ptbl-base-v2_6_19_min.json (43)

- **Depended on by**: None

#### Top-level structure

| Key | Required | Type | Meaning |
| --- | --- | --- | --- |
| integrations | No | object |  |
| notifications | No | $ref |  |
| realtime | No | $ref |  |
| billing | No | $ref |  |
| payments | No | $ref |  |
| approval_workflows | No | $ref |  |
| batch_operations | No | $ref |  |
| file_processing | No | $ref |  |
| content | No | $ref |  |
| voice | No | $ref |  |
| code_execution | No | $ref |  |
| ai_generation | No | $ref |  |
| outbound_webhooks | No | $ref |  |
| feature_flags | No | $ref |  |

#### Key definitions

| Definition | Notes |
| --- | --- |
| ApprovalWorkflowsConfig |  |
| VoiceConfig |  |
| RealtimeConfig |  |
| PaymentsConfig |  |
| OutboundWebhooksConfig |  |
| NotificationsConfig |  |
| Integration |  |
| FileProcessingConfig |  |
| FeatureFlagsConfig |  |
| ContentConfig |  |
| CodeExecutionConfig |  |
| BillingConfig |  |
| BatchOperationsConfig |  |
| AIGenerationConfig |  |

#### Minimal valid skeleton (shape guide)

{}

#### Common pitfalls

- Never inline credentials. Always use SecretRef for sensitive values.

- Prefer explicit retry and rate limiting options over generic bags where possible.

### ptbl-app-security-v2_6_19_min.json

- **Title**: PTBL App Security Schema

- **Role**: Authored manifest

- **Scope**: Auth, policies, security posture and data protection

- **Produced by**: LLM generator or security authors

- **Consumed by**: Policy engine; authz enforcement

- **$id**: https://prompt.build/ptbl/2.6.19/app-security

Enterprise security configuration

#### Dependencies

- **Depends on**: ptbl-base-v2_6_19_min.json (68)

- **Depended on by**: None

#### Top-level structure

| Key | Required | Type | Meaning |
| --- | --- | --- | --- |
| security | Yes | $ref |  |

#### Key definitions

| Definition | Notes |
| --- | --- |
| AgentSecurityConfig | Security configuration for on-premises agents |
| PKIConfig | Public Key Infrastructure and certificate management |
| DataProtectionConfig | Data classification, masking, tokenization, and DLP |
| SecurityConfig | Comprehensive enterprise security configuration |
| SecurityTestingConfig | Security testing and scanning configuration |
| IncidentResponseConfig | Security incident detection and response |
| ZeroTrustConfig | Zero Trust Architecture configuration |
| ComplianceConfig | Compliance and privacy configuration |
| CertificateConfig | Individual certificate configuration |
| ApplicationSecurityConfig | OWASP and application-level security |
| InfrastructureSecurityConfig | Infrastructure and network security |
| AuthenticationConfig | Authentication configuration |
| AuditConfig | Comprehensive audit logging |
| SecretsConfig |  |
| RowLevelPolicy |  |
| Role |  |
| Policy |  |
| Permission |  |

#### Minimal valid skeleton (shape guide)

```json
{
  "security": "<value>"
}
```

#### Common pitfalls

- Avoid policy rules that are ambiguous. Prefer explicit policy types.

- Keep SecretRef usage consistent for keys and credentials.

### ptbl-changeset-v2_6_19_min.json

- **Title**: PTBL Changeset Schema

- **Role**: Operational artifact

- **Scope**: Structured edits, impact analysis, apply and rollback

- **Produced by**: Editors and planning agents

- **Consumed by**: Apply engine; validators; audit

- **$id**: https://prompt.build/ptbl/2.6.19/changeset

Formal change plan structure. Instead of direct edits, changes go through: plan -> impact analysis -> validation -> apply.

#### Dependencies

- **Depends on**: ptbl-base-v2_6_19_min.json (17)

- **Depended on by**: None

#### Top-level structure

| Key | Required | Type | Meaning |
| --- | --- | --- | --- |
| ptbl_changeset | Yes | string | Changeset format version |
| id | Yes | string | Unique changeset ID (e.g., cs-abc12345) |
| created_at | Yes | string |  |
| author | No | object |  |
| status | Yes | string | Current status in the change workflow |
| title | No | string | Short description of what this changeset does |
| description | No | string | Detailed explanation of the change |
| rationale | No | string | Why this change is being made |
| ticket | No | string | Reference to issue/ticket/user request (e.g., JIRA-123, GH-456, #789) |
| related_adr | No | string | ADR ID if this change implements an architecture decision |
| changes | Yes | array | List of changes to apply |
| impact | No | $ref | Result of impact analysis (populated after analysis) |
| validation | No | $ref | Result of validation (populated after validation) |
| execution | No | $ref | Result of applying the changeset (populated after apply) |
| rollback | No | object | Rollback information if changeset was rolled back |
| granular_changes | No | array | Detailed breakdown of each atomic change |
| regeneration_plan | No | $ref | Computed plan for how to apply changes |
| can_diff | No | boolean | Quick check: can this changeset be applied via diff (true) or needs regen (false) |

#### Key definitions

| Definition | Notes |
| --- | --- |
| ChangeClassification | How this change affects regeneration: additive=diff only, breaking=full regen |
| GranularChange | A single atomic change with full context for diff vs regen decision |
| RegenerationPlan | The execution plan: what to diff vs fully regenerate |
| ImpactAnalysis | Result of analyzing what this changeset affects |
| _patch_guidance | Guidance on patch operations in PTBL |
| ValidationResult | Result of validating the changeset |
| ExecutionResult | Result of applying the changeset |
| Change |  |
| AffectedArtifact |  |

#### Minimal valid skeleton (shape guide)

```json
{
  "ptbl_changeset": "<string>",
  "id": "<string>",
  "created_at": "<string>",
  "status": "<string>",
  "changes": []
}
```

#### Common pitfalls

- Prefer patch operations over full regeneration when edits are localized.

- Record validation results and execution outcomes for auditability.

### ptbl-index-v2_6_19_min.json

- **Title**: PTBL Index Schema

- **Role**: Generated artifact

- **Scope**: Workspace index and reverse dependencies

- **Produced by**: Index generator

- **Consumed by**: Editors; impact analysis; tooling

- **$id**: https://prompt.build/ptbl/2.6.19/index

Generated index for fast lookups. Maps UIDs to locations (including JSON Pointers) and tracks all references. Enables 'what depends on X' queries.

#### Dependencies

- **Depends on**: ptbl-base-v2_6_19_min.json (44)

- **Depended on by**: None

#### Top-level structure

| Key | Required | Type | Meaning |
| --- | --- | --- | --- |
| ptbl_index | Yes | string | Index format version |
| generated_at | Yes | string |  |
| generated_from | No | object |  |
| workspace | Yes | object | Workspace-level metadata |
| modules | No | object | Module index: uid -> location and metadata |
| entities | No | object | Entity index: uid -> location and references |
| fields | No | object | Field index: 'entity_uid.field_name' -> references |
| apis | No | object | API index: uid -> location and references |
| workflows | No | object | Workflow index: uid -> location and references |
| agents | No | object | Agent index: uid -> location and references |
| dependency_graph | No | object | Full dependency graph at all levels |
| reverse_index | No | object | Reverse lookup: for each UID, what references it |

#### Key definitions

| Definition | Notes |
| --- | --- |
| WorkflowIndexEntry |  |
| AgentIndexEntry |  |
| ModuleIndexEntry |  |
| FieldIndexEntry |  |
| EntityIndexEntry |  |
| ApiIndexEntry |  |

#### Minimal valid skeleton (shape guide)

```json
{
  "ptbl_index": "<string>",
  "generated_at": "<string>",
  "workspace": {}
}
```

#### Common pitfalls

- This file is generated and should not be hand-authored.

- Indexes must be regenerated after changesets are applied.

### ptbl-lock-v2_6_19_min.json

- **Title**: PTBL Lock Schema

- **Role**: Generated artifact

- **Scope**: Pinned resolved module references and integrity hashes

- **Produced by**: Resolver tooling

- **Consumed by**: Compiler; build reproducibility

- **$id**: https://prompt.build/ptbl/2.6.19/lock

Schema for PTBL lockfiles. Generated artifact that captures resolved dependency versions and integrity hashes for reproducible builds.

#### Dependencies

- **Depends on**: ptbl-base-v2_6_19_min.json (6)

- **Depended on by**: None

#### Top-level structure

| Key | Required | Type | Meaning |
| --- | --- | --- | --- |
| ptbl_lock | Yes | string | Lock file format version |
| generated_at | Yes | string | When this lockfile was generated |
| generated_by | No | object |  |
| app | Yes | object |  |
| resolved | Yes | object | Map of module reference to resolved module info. Discriminated by 'source' field. |
| dependency_graph | No | object | Adjacency list representation of module dependencies |
| checksums | No | object | Additional file checksums for integrity verification |
| resolution_metadata | No | object |  |

#### Minimal valid skeleton (shape guide)

```json
{
  "ptbl_lock": "<string>",
  "generated_at": "<string>",
  "app": {},
  "resolved": {}
}
```

#### Common pitfalls

- This file is generated. Treat manual edits as suspect. Prefer re-running resolution tooling.

- For git sources, include git_commit when possible for true reproducibility.

### ptbl-module-v2_6_19_min.json

- **Title**: PTBL Module Schema

- **Role**: Authored manifest

- **Scope**: Reusable modules: entities, APIs, workflows, agents, events, migrations

- **Produced by**: LLM generator or module authors

- **Consumed by**: Apps via imports; compiler; validators

- **$id**: https://prompt.build/ptbl/2.6.19/module

PTBL module manifests. v2.6.19: module.uid is canonical (no slug).

#### Dependencies

- **Depends on**: ptbl-base-v2_6_19_min.json (31)

- **Depended on by**: None

#### Top-level structure

| Key | Required | Type | Meaning |
| --- | --- | --- | --- |
| ptbl | Yes | string | PTBL schema version |
| generated_by | No | object |  |
| module | Yes | object |  |
| imports | No | array | Other modules this module depends on |
| entities | No | object | Entities definitions. Map key IS the StableUID. Values do NOT contain uid. |
| enums | No | object | Enumeration types |
| apis | No | object | Apis definitions. Map key IS the StableUID. Values do NOT contain uid. |
| workflows | No | object | Workflows definitions. Map key IS the StableUID. Values do NOT contain uid. |
| agents | No | object | Agents definitions. Map key IS the StableUID. Values do NOT contain uid. |
| events | No | object | Events definitions. Map key IS the StableUID. Values do NOT contain uid. |
| queues | No | object | Queues definitions. Map key IS the StableUID. Values do NOT contain uid. |
| jobs | No | object | Jobs definitions. Map key IS the StableUID. Values do NOT contain uid. |
| tests | No | $ref | Module-level tests |
| migrations | No | array | Schema migrations for this module |

#### Key definitions

| Definition | Notes |
| --- | --- |
| MigrationStep | Migration step. Discriminated by 'type' field. |
| ModuleTestConfig |  |
| Migration |  |
| Import |  |

#### Minimal valid skeleton (shape guide)

```json
{
  "ptbl": "<string>",
  "module": {}
}
```

#### Common pitfalls

- Keep entities, APIs, workflows, and agents addressable via StableUID map keys.

- Migrations should be machine-executable. Avoid free-form text steps.

## 9. Python tooling reference

These scripts enforce schema quality and protect against regressions. They are required gates for releases.

### ptbl_lint_v2_6_19.py

How to run:

python3 ptbl_lint_v2_6_19.py 2.6.19 ptbl-*-v2_6_19_min.json

What it checks:

- Schema strictness and open-object bypasses

- Discriminated union correctness

- Version drift, $id consistency, and $ref hygiene

- Examples sanity to prevent copy-paste invalid shapes

### ptbl_schema_meta_tests.py

How to run:

python3 ptbl_schema_meta_tests.py ptbl-*-v2_6_19_min.json

What it checks:

- Schema-shape invariants across files (duration and schedule typing)

- Pattern checks for known ambiguous fields

- Consistency rules that are hard to express directly in JSON Schema

### ptbl_schema_regression_tests.py

How to run:

python3 ptbl_schema_regression_tests.py ptbl-*-v2_6_19_min.json

What it checks:

- Curated instance fixtures for previously fixed bugs

- Failing fixtures that must remain invalid

- Positive fixtures that must remain valid

## Appendix A. Quickstart commands

# Lint gate
python3 ptbl_lint_v2_6_19.py 2.6.19 ptbl-*-v2_6_19_min.json
# Meta tests (schema-shape invariants)
python3 ptbl_schema_meta_tests.py ptbl-*-v2_6_19_min.json
# Regression tests (instance fixtures)
python3 ptbl_schema_regression_tests.py ptbl-*-v2_6_19_min.json

## Appendix B. Changelog pointer

See CHANGELOG-v2_6_19.md in the package for the authoritative release notes.

