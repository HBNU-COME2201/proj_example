from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
import yaml
from pydantic import ValidationError
from pydantic import BaseModel, Field, create_model
from .schemas.prompt_spec import BasePromptSpec, DerivedPromptSpec, Sections
from .core import Prompt, SlotSchema
from .sections import SystemSection, InstructionSection, ConstraintSection, ExampleSection

def _make_slot_schema(varspec: Dict[str, Any]) -> type[SlotSchema]:
    fields = {}
    for k, v in varspec.items():
        tmap = {"string": str, "int": int, "float": float, "bool": bool}
        t = tmap[v.type]
        default = ... if v.required else None
        fkwargs = {}
        for attr in ("min_length","max_length","ge","le"):
            val = getattr(v, attr, None)
            if val is not None:
                fkwargs[attr] = val
        fields[k] = (t, Field(default, **fkwargs))
    model = create_model("DynamicSlots", __base__=SlotSchema, **fields)  # type: ignore
    return model

def _build_sections(sections: Sections):
    return [
        SystemSection(text=sections.system),
        InstructionSection(template=sections.instruction),
        ConstraintSection(bullets=sections.constraints or []),
        ExampleSection(examples=sections.examples or []),
    ]

def build_from_folder(folder: str | Path) -> Dict[str, Prompt]:
    folder = Path(folder)
    bases: Dict[str, BasePromptSpec] = {}
    derived: Dict[str, DerivedPromptSpec] = {}

    for p in folder.glob("*.yaml"):
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        if data.get("type") == "base":
            b = BasePromptSpec(**data)
            bases[b.name] = b
        elif data.get("type") == "derived":
            d = DerivedPromptSpec(**data)
            derived[d.name] = d
        else:
            raise ValueError(f"Unknown type in {p}")

    resolved: Dict[str, Prompt] = {}

    def merge_sections(base: Sections, overrides: dict | None) -> Sections:
        s = base.model_copy(deep=True)
        if not overrides:
            return s
        if "system" in overrides and overrides["system"] is not None:
            s.system = overrides["system"]
        if "instruction" in overrides and overrides["instruction"] is not None:
            s.instruction = overrides["instruction"]
        def apply_list(key: str):
            patch = overrides.get(key)
            if not patch:
                return getattr(s, key)
            lst = list(getattr(s, key) or [])
            if "replace" in patch and patch["replace"] is not None:
                lst = list(patch["replace"])
            if "append" in patch:
                lst += list(patch["append"])
            if "remove" in patch:
                rm = set(patch["remove"])
                lst = [x for x in lst if x not in rm]
            return lst
        s.constraints = apply_list("constraints")
        s.examples = apply_list("examples")
        return s

    def resolve(name: str) -> Prompt:
        if name in resolved:
            return resolved[name]
        if name in bases:
            bp = bases[name]
            slot_model = _make_slot_schema(bp.variables)
            pr = Prompt(name=bp.name, version="v1",
                        sections=_build_sections(bp.sections),
                        slot_schema=slot_model, parser=None)
            resolved[name] = pr
            return pr
        if name in derived:
            dv = derived[name]
            base_name = dv.base
            if base_name not in bases:
                if base_name in derived:
                    _ = resolve(base_name)  # ensure base is built
                    # convert resolved base Prompt to BasePromptSpec surrogate:
                    # for simplicity require that base_name is base, else raise
                    raise ValueError("Derived-of-derived is not supported in this minimal manager.")
                raise KeyError(f"Unknown base: {base_name}")
            bspec = bases[base_name]
            merged_vars = dict(bspec.variables)
            if dv.variables:
                for k, v in dv.variables.items():
                    merged_vars[k] = v
            merged_sections = merge_sections(bspec.sections, (dv.overrides or {}).get("sections"))
            slot_model = _make_slot_schema(merged_vars)
            pr = Prompt(name=dv.name, version="v1",
                        sections=_build_sections(merged_sections),
                        slot_schema=slot_model, parser=None)
            resolved[name] = pr
            return pr
        raise KeyError(f"Unknown prompt: {name}")

    for k in list(bases.keys()) + list(derived.keys()):
        resolve(k)

    return resolved
