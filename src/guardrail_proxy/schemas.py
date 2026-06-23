# src/guardrail_proxy/schemas.py
from pydantic import BaseModel, Field


class GuardrailEvaluation(BaseModel):
    safe: bool = Field(description="True if output adheres to policies, False otherwise.")
    reason: str = Field(description="Deterministic validation or failure reason summary.")
