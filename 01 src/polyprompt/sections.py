from __future__ import annotations
from dataclasses import dataclass
from typing import List
from .core import Section

@dataclass(frozen=True)
class SystemSection(Section):
    role: str = "system"
    text: str = "You are a helpful assistant."
    def render(self, slots):
        return f"[{self.role.upper()}]\n{self.text}"

@dataclass(frozen=True)
class InstructionSection(Section):
    template: str = "Do X with {topic}."
    def render(self, slots):
        return self.template.format(**slots)

@dataclass(frozen=True)
class ConstraintSection(Section):
    bullets: List[str] = ()
    def render(self, slots):
        if not self.bullets:
            return ""
        lines = "\n".join(f"- {b}" for b in self.bullets)
        return f"Constraints:\n{lines}"

@dataclass(frozen=True)
class ExampleSection(Section):
    examples: List[str] = ()
    def render(self, slots):
        if not self.examples:
            return ""
        return "Examples:\n" + "\n\n".join(self.examples)
