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
