from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProcessRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    problem: str = Field(min_length=1, max_length=10_000)
    mode: Literal["sequential", "parallel"] = "sequential"
    api_key: str | None = Field(default=None, min_length=1, max_length=1_000)
    model: str = Field(default="gemini-3-flash-preview", min_length=1, max_length=200)

    @field_validator("api_key")
    @classmethod
    def empty_api_key_is_none(cls, value):
        return value or None


class ReasoningStep(BaseModel):
    step: int
    thought: str
    confidence: float = Field(ge=0, le=1)
    evidence: list[str]


class AlternativePath(BaseModel):
    reasoning: str
    why_rejected: str
    confidence: float = Field(ge=0, le=1)


class SignatureResponse(BaseModel):
    reasoning_chain: list[ReasoningStep] = Field(min_length=1)
    conclusion: str = Field(min_length=1)
    confidence_score: float = Field(ge=0, le=1)
    alternative_paths: list[AlternativePath] = Field(default_factory=list)
