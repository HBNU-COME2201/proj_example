from __future__ import annotations
import json, yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

@dataclass
class PromptObject:
    name: str
    version: str
    template: str
    variables: Dict[str, dict]
    constraints: List[str]
    examples: List[str]
    meta: Dict[str, Any]

def load_yaml_files(folder: str | Path) -> Dict[str, dict]:
    folder = Path(folder)
    specs = {}
    for p in folder.glob("*.yaml"):
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        specs[data["name"]] = data
    return specs

def _merge_two(base: dict, derived: dict) -> dict:
    out = json.loads(json.dumps(base))
    out["name"] = derived["name"]
    if "variables" in derived:
        out.setdefault("variables", {})
        out["variables"].update(derived["variables"])
    out.setdefault("sections", {})
    sec = out["sections"]
    dsec = (derived.get("overrides", {}) or {}).get("sections", {})
    for k in ("system","instruction"):
        if k in dsec: sec[k] = dsec[k]
        if "sections" in derived and k in derived["sections"]:
            sec[k] = derived["sections"][k]
    for key in ("constraints","examples"):
        lst = list(sec.get(key) or [])
        if "sections" in derived and key in derived["sections"]:
            val = derived["sections"][key]
            if isinstance(val, list): lst = list(val)
        if key in dsec:
            patch = dsec[key]
            if "replace" in patch and patch["replace"] is not None:
                lst = list(patch["replace"])
            if "append" in patch:
                lst += list(patch["append"])
            if "remove" in patch:
                rm = set(patch["remove"])
                lst = [x for x in lst if x not in rm]
        sec[key] = lst
    if "output" in derived:
        out.setdefault("output", {})
        out["output"].update(derived["output"])
    return out

def build_prompts(folder: str | Path, version: str = "v1") -> Dict[str, PromptObject]:
    folder = Path(folder)
    raw = {}
    for p in folder.glob("*.yaml"):
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        raw[d["name"]] = d
    resolved = {}
    def res(name: str) -> dict:
        if name in resolved: return resolved[name]
        spec = raw[name]
        if spec["type"] == "base":
            resolved[name] = spec
            return spec
        base = res(spec["base"])
        merged = _merge_two(base, spec)
        resolved[name] = merged
        return merged
    for k in list(raw.keys()):
        res(k)
    out = {}
    for n, s in resolved.items():
        sec = s.get("sections", {})
        blocks = []
        if sec.get("system"): blocks.append(f"[SYSTEM]\n{sec['system']}")
        if sec.get("instruction"): blocks.append(sec["instruction"])
        if sec.get("constraints"):
            blocks.append("Constraints:\n" + "\n".join(f"- {c}" for c in sec["constraints"]))
        if sec.get("examples"):
            blocks.append("Examples:\n" + "\n\n".join(sec["examples"]))
        tmpl = "\n\n".join(b for b in blocks if b.strip())
        po = PromptObject(
            name=n, version=version, template=tmpl,
            variables=s.get("variables", {}),
            constraints=sec.get("constraints", []) or [],
            examples=sec.get("examples", []) or [],
            meta={"output": s.get("output", {}), "description": s.get("description", "")}
        )
        out[n] = po
    return out

def render(po: PromptObject, **slots) -> str:
    return po.template.format(**slots)
