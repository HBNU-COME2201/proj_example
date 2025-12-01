# specification.md — Technical Specification (PolyPrompt)

## 1. Scope
PolyPrompt provides a typed, immutable, and testable representation of prompts as Python objects, with Base/Derived YAML specifications compiled into `Prompt` instances. The system targets reproducible experiments, safe reuse, and governed specialization.

## 2. Conceptual Model
- Prompt (immutable):
  - `name: str`, `version: str`
  - `sections: List[Section]` (Composite)
  - `slot_schema: Type[SlotSchema]` (Pydantic-generated)
  - `parser: Optional[Parser]` (Strategy)
- Section types:
  - `SystemSection(text)`, `InstructionSection(template)`
  - `ConstraintSection(bullets: List[str])`, `ExampleSection(examples: List[str])`
- Strategies:
  - `Inferencer.generate(prompt: str, **kw) -> str`
  - `Parser.parse(str) -> Any`, `Parser.validate(Any) -> Any`

## 3. YAML Specifications
### 3.1 Base Prompt (Required fields)
```yaml
type: base
name: <string>
description: <string>
variables: { <name>: {type, required, [min_length|max_length|ge|le], [override]} }
sections:
  system: <string>
  instruction: <string>
  constraints: [<string>...]
  examples: [<string>...]
output:
  format: free_text|json
  schema: <JSON-Schema or null>
```
### 3.2 Derived Prompt (Required fields)
```yaml
type: derived
name: <string>
base: <base_name>
description: <string?>    # optional
variables: { ... }        # optional; default = inherit; policy = strengthen
overrides:
  sections:
    system: <replace_str?>
    instruction: <replace_str?>
    constraints: { replace?: [..], append?: [..], remove?: [..] }
    examples:    { replace?: [..], append?: [..], remove?: [..] }
  output:
    format: free_text|json
    schema: <JSON-Schema or null>
```

## 4. Validation Semantics
- Variable typing: `string|int|float|bool`, `required` controls default presence.
- Strengthening by default (e.g., `ge`↑, `le`↓, `min_length`↑, `max_length`↓).
- Relaxation requires `override: true`.
- Section merge precedence: `replace` > `append/remove`; empty `replace` is an error.

## 5. Compilation Pipeline
1. Load all `*.yaml` under `prompts/`.
2. Parse as BasePromptSpec or DerivedPromptSpec (Pydantic).
3. Index bases; resolve derived → base references (no cycles).
4. Construct dynamic `SlotSchema` via `pydantic.create_model(...)`.
5. Materialize Section objects per merged spec.
6. Produce `Prompt(name, version, sections, slot_schema, parser)`.

## 6. Inference & Post-processing
- `Prompt.render(**slots)` validates and interpolates strings.
- `Prompt.infer(inferencer, **slots)` calls backend and applies parser if set:
  - `output.format=json` → JSON parsing and optional JSON-Schema validation.
- Backends are injected; `Prompt` remains provider-agnostic.

## 7. Error Handling
- YAML schema errors → `ValidationError`.
- Unknown base → `KeyError` with filename and base name.
- Slot validation failure → `ValueError` with field diagnostics.
- Merge conflicts (e.g., undefined variable in template) → descriptive error.

## 8. Testing Requirements
- Snapshot tests: canonical inputs for each prompt ensure render stability.
- Negative tests: invalid slot types/constraints must raise.
- YAML compile tests: folder-level `build_from_folder` E2E tests.
- Parser tests (if `format=json`): valid/invalid payloads.

## 9. Performance & Limits
- Rendering ~ O(n) over sections; YAML loading linear in file count.
- Token budgeting handled outside core (at strategy or preprocessing).

## 10. Security & Compliance
- No secrets in YAML; use env or runtime slots.
- For PII, add policy constraints and masking in a custom parser/validator.
- Respect third-party model ToS; keep MIT headers on distribution.

## 11. Extension Points
- New Section types (Citation/StyleGuide/Policy).
- Domain parsers (PEG/Regex/JSON-Schema) and evaluation plug-ins.
- CLI: `pp build`, `pp render`, `pp infer`.

## 12. Versioning
- Identity = `name:version`. Bump `version` when semantics/constraints change.
- Maintain `docs/CHANGELOG.md` per prompt `name:version`.
