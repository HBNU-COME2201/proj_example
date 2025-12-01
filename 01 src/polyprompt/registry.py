from __future__ import annotations
from typing import Dict
from .core import Prompt

class PromptRegistry:
    _reg: Dict[str, Prompt] = {}
    @classmethod
    def add(cls, prompt: Prompt):
        key = f"{prompt.name}:{prompt.version}"
        if key in cls._reg:
            raise KeyError(f"duplicate {key}")
        cls._reg[key] = prompt
    @classmethod
    def get(cls, name: str, version: str = "v1") -> Prompt:
        key = f"{name}:{version}"
        if key not in cls._reg:
            raise KeyError(f"not found {key}")
        return cls._reg[key]
    @classmethod
    def all(cls) -> Dict[str, Prompt]:
        return dict(cls._reg)
