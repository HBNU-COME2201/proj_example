# acceptance.md — Acceptance Criteria & Test Plan (PolyPrompt)

## A. Functional Acceptance Criteria
1. YAML Loading & Typing
   - AC-1.1: Parse all `*.yaml` under `prompts/` as `base` or `derived`.
   - AC-1.2: Base requires `name, description, variables, sections`.
   - AC-1.3: Derived requires `name, base`.
   - AC-1.4: Typed slots enforced via dynamic Pydantic models.

2. Inheritance & Overrides
   - AC-2.1: Derived inherits variables and sections from base.
   - AC-2.2: Strengthen-by-default; relaxation requires `override: true`.
   - AC-2.3: `replace`, `append`, `remove` supported for list sections.
   - AC-2.4: Cyclic inheritance rejected with clear error.

3. Rendering & Inference
   - AC-3.1: `render(**slots)` validates and interpolates all variables.
   - AC-3.2: `infer(inferencer, **slots)` calls backend once and returns raw or parsed output.
   - AC-3.3: With `output.format=json`, invalid JSON raises with diagnostics.

4. Immutability & Idempotency
   - AC-4.1: `Prompt` and `Section` instances are frozen (immutable).
   - AC-4.2: Repeated `render()` calls with identical inputs are byte-identical.

5. Registry & Discovery
   - AC-5.1: Built prompts MAY be registered as `name:version` and retrievable.
   - AC-5.2: Unknown `name:version` raises `KeyError` with helpful message.

## B. Non-Functional Acceptance Criteria
- NFR-1: Unit test coverage ≥ 80% for core modules.
- NFR-2: Lint clean (`ruff`); public interfaces carry type hints.
- NFR-3: Documentation (README, design, this doc) present and accurate.
- NFR-4: Clean environment passes `pytest -q` on first run.

## C. Representative Test Cases
- C.1 Snapshot Render (Base): check wording and idempotency.
- C.2 Derived Merge & Policy: verify system text and constraints append; enforce strengthened bounds.
- C.3 Slot Validation Errors: invalid length triggers `ValueError`.
- C.4 JSON Parsing: invalid JSON raises; include prompt `name:version` in message.
- C.5 Inheritance Cycle: two derived referencing each other must fail.

## D. Test Automation
- `tests/test_yaml_compile.py`: build from `prompts/`, assert names and render snapshots.
- `tests/test_parser_json.py`: valid/invalid JSON with schema checks (if applicable).
- CI: `ruff`, `pytest -q`, optional `mypy`; cache dependencies for speed.

## E. Acceptance Procedure
1. Setup per `instruction.md`.
2. Run `pytest -q`; verify all tests pass and coverage meets NFR-1.
3. Inspect snapshots for base/derived prompts.
4. Manual render of one prompt; compare with spec.
5. Approve merge & tag `v0.1.0`; update `docs/CHANGELOG.md`.
