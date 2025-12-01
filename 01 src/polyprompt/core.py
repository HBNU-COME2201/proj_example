from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Protocol, runtime_checkable, Optional, Type
from pydantic import BaseModel, ValidationError

# -------- Sections --------
@dataclass(frozen=True)
class Section:
    def render(self, slots: Dict[str, Any]) -> str:
        raise NotImplementedError

@dataclass(frozen=True)
class TextSection(Section):
    text: str
    def render(self, slots: Dict[str, Any]) -> str:
        return self.text.format(**slots)

# -------- Slots --------
class SlotSchema(BaseModel):
    pass

# -------- Strategies --------
@runtime_checkable
class Inferencer(Protocol):
    def generate(self, prompt: str, **kwargs) -> str: ...

@runtime_checkable
class Parser(Protocol):
    def parse(self, text: str) -> Any: ...
    def validate(self, obj: Any) -> Any: ...

# -------- Prompt --------
@dataclass(frozen=True)
class Prompt:
    name: str
    version: str = "v1"
    sections: List[Section] = field(default_factory=list)
    slot_schema: Type[SlotSchema] = SlotSchema
    parser: Optional[Parser] = None

    def render(self, **slots) -> str:
        try:
            valid = self.slot_schema(**slots)
        except ValidationError as e:
            raise ValueError(f"Slot validation failed: {e}") from e
        data = valid.model_dump()
        parts = [s.render(data) for s in self.sections]
        return "\n\n".join([p for p in parts if str(p).strip()])

    def infer(self, inferencer: Inferencer, **slots) -> Any:
        text = self.render(**slots)
        raw = inferencer.generate(text, prompt_name=self.name, version=self.version)
        if self.parser:
            parsed = self.parser.parse(raw)
            return self.parser.validate(parsed)
        return raw

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["slot_schema"] = self.slot_schema.__name__
        d["parser"] = self.parser.__class__.__name__ if self.parser else None
        d["sections"] = [s.__class__.__name__ for s in self.sections]
        return d
