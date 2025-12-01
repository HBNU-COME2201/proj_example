# instruction.md — Project Operating Instructions (PolyPrompt)

## 1. Purpose
This document prescribes how to operate, extend, and review the PolyPrompt project, which models “prompt as a Python object” and supports YAML-defined Base/Derived prompts compiled into immutable `Prompt` instances.

## 2. Audience
- Research engineers designing prompt libraries and experiments
- Software engineers maintaining CI/CD pipelines and package releases
- Instructors using PolyPrompt in coursework or internal training

## 3. Prerequisites
- Python ≥ 3.10, `pip`, optional `uv`/`poetry`
- Familiarity with OOP (encapsulation, inheritance, composition, polymorphism)
- Basic YAML and Pydantic usage

## 4. Quick Start
```bash
git clone <YOUR_REPO_URL> polyprompt && cd polyprompt
python -m venv .venv && . .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -e .[dev]
pytest -q
python examples/run_summarize.py
```

## 5. Directory Layout (Reference)
```
src/polyprompt/
  core.py           # Prompt, Section, SlotSchema
  sections.py       # System/Instruction/Constraint/Example
  strategies.py     # Inferencer/Parser strategies
  registry.py       # PromptRegistry
  prompts.py        # Example objects (optional)
  prompt_manager.py # YAML loader/merger/compiler
  schemas/
    prompt_spec.py  # Pydantic specs for Base/Derived YAML

prompts/
  *.yaml            # Base/Derived prompt specs

tests/
  test_summarize.py
  test_yaml_compile.py      # (add after YAML manager is enabled)
```

## 6. Authoring Prompts (YAML → Object)
1. Create Base YAML (e.g., `prompts/summarize.base.yaml`) with required fields:
   - `type: base`, `name`, `description`, `variables`, `sections`, `output`
2. Create Derived YAML when specialization is needed (e.g., `prompts/summarize.legal.yaml`):
   - `type: derived`, `name`, `base`, optional `description`, `variables`, `overrides`
3. Build and retrieve compiled prompts:
```python
from polyprompt.prompt_manager import build_from_folder
prompts = build_from_folder("prompts")
p = prompts["summarize.legal"]
txt = p.render(text="...", length=80)
```
4. Use an Inferencer for generation:
```python
from polyprompt.strategies import OpenAIInferencer
out = p.infer(OpenAIInferencer(client=None), text="...", length=80)
```

## 7. Variable and Section Policies
- Variables: strengthening constraints is default; relaxation requires `override: true`.
- Sections: use `replace` (default), or `append/remove` for `constraints/examples`; `system/instruction` may be replaced directly.
- Output: if `output.format=json`, wire a JSON parser/validator strategy in `prompt_manager.py`.

## 8. Code Style & Reviews
- Follow PEP8 and keep functions pure when feasible.
- Sections must be idempotent renderers; avoid external state in `render()`.
- Ensure immutability of `Prompt`/`Section` dataclasses (`frozen=True`).
- Mandatory unit tests for new prompts: snapshot of `render()` and validation failure cases.

## 9. CI/CD
- Lint: `ruff`, Type-check: `mypy` (optional), Test: `pytest -q`
- Enforce snapshot tests on PR; diff of rendered text must be reviewed by a human.
- Release via `build` → `twine` or internal registry. Keep changelog by prompt `name:version`.

## 10. Security & Governance
- Sensitive strings must not be hard-coded in YAML; pass via slots or env.
- If PII may appear in slots, add a policy constraint section (masking rules) and a validator.
- License and third-party model usage must respect provider ToS.

## 11. Troubleshooting
- ValidationError: check `variables` in YAML and slot input types.
- KeyError (prompt not found): confirm `name` and `base`; run `build_from_folder()`.
- Token overflow: shorten `sections` or add summarization/constraint logic.
