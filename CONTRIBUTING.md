# Contributing

MBP is a draft. Contributions are welcome as pull requests.

## Before proposing a change

1. Read [`SPEC.md`](SPEC.md) and the relevant [`docs/`](docs/) policy.
2. Check whether the change is a clarification (no version bump) or a behavior change (version bump + changelog).
3. If the change affects a schema, update the schema and any example that validates against it.

## Change types

- **Clarification:** wording, examples, docs. No version bump.
- **Addition:** new optional field, new policy section. Minor bump.
- **Breaking:** removed field, changed semantics, changed freeze rules. Major bump (pre-1.0: minor bump + explicit changelog).

## Validation

A PR SHOULD include:

- the updated `CHANGELOG.md` entry,
- validation that all examples still conform to their schemas,
- a note if any reference implementation needs to update its `protocol_version`.

## Style

- Engineering tone. No marketing claims ("new industry standard", "best", "leading").
- Specifications are normative; examples are illustrative.
- Chinese summaries are welcome where they aid comprehension, but the normative text is English.
