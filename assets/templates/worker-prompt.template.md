# Worker Task: {{workorder_id}}

## Identity

- Workorder: `{{workorder_id}}`
- Todo: `{{todo_id}}`
- Repository / worktree: `{{repository_or_worktree}}`
- Branch: `{{branch}}`
- Base: `{{base}}`

## Allowed Files

```text
{{allowed_files}}
```

## Forbidden Changes

```text
{{forbidden_changes}}
```

## Behavior Boundary

{{behavior_boundary}}

## Architecture And Configuration Boundary

- Architecture: `{{architecture_boundary}}`
- Configuration: `{{configuration_boundary}}`

Do not add business logic to an identified monolith. Do not bypass the declared adapter/gateway boundary. Do not introduce configuration sources, defaults, or precedence changes outside this boundary.

## Implementation Requirements

{{implementation_requirements}}

## Acceptance

```bash
{{acceptance_commands}}
```

## Output

Write the result to:

```text
{{output_location}}
```

The output must include:

1. Changed files.
2. Acceptance commands and results.
3. Behavior change.
4. Architecture impact.
5. Configuration impact.
6. Findings outside scope.
7. Incomplete work and reason.

## Stop Conditions

Stop and report instead of improvising when:

1. A required file is missing.
2. A change outside `Allowed Files` is necessary.
3. An acceptance command cannot run.
4. The workorder conflicts with another task.
5. Evidence is insufficient for a completion conclusion.

## Hard Prohibitions

Do not allocate IDs, modify the shared registry, merge branches, or claim completion without recorded acceptance results. Do not add business logic to an identified monolith, bypass the declared adapter/gateway boundary, scatter configuration, or introduce compatibility without a removal condition.
