from __future__ import annotations
from pydantic import BaseModel
from typing import Dict, Optional, List, Literal, Any

VarType = Literal["string", "int", "float", "bool"]

class VariableSpec(BaseModel):
    type: VarType = "string"
    required: bool = True
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    ge: Optional[float] = None
    le: Optional[float] = None
    override: bool = False

class Sections(BaseModel):
    system: str
    instruction: str
    constraints: List[str] = []
    examples: List[str] = []

class OutputSpec(BaseModel):
    format: Literal["free_text","json"] = "free_text"
    schema: Optional[Dict[str, Any]] = None

class BasePromptSpec(BaseModel):
    type: Literal["base"] = "base"
    name: str
    description: str
    variables: Dict[str, VariableSpec]
    sections: Sections
    output: OutputSpec = OutputSpec()

class DerivedPromptSpec(BaseModel):
    type: Literal["derived"] = "derived"
    name: str
    base: str
    description: Optional[str] = None
    variables: Optional[Dict[str, VariableSpec]] = None
    overrides: Optional[Dict[str, Any]] = None
