from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


Operation = Literal["tn", "itn", "num2words"]
Num2WordsMode = Literal["cardinal", "ordinal", "ordinal_num", "year", "currency"]


class TNOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ITNOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Num2WordsOptions(BaseModel):
    mode: Num2WordsMode = "cardinal"
    currency: str | None = Field(default=None, max_length=8)


class TNRequest(BaseModel):
    text: str = Field(min_length=1)
    language: str = "zh"
    options: TNOptions = Field(default_factory=TNOptions)


class ITNRequest(BaseModel):
    text: str = Field(min_length=1)
    language: str = "zh"
    options: ITNOptions = Field(default_factory=ITNOptions)


class Num2WordsRequest(BaseModel):
    number: str = Field(min_length=1)
    language: str = "en"
    options: Num2WordsOptions = Field(default_factory=Num2WordsOptions)


class ProcessResponse(BaseModel):
    operation: Operation
    language: str
    input: str
    output: str
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class BatchRequest(BaseModel):
    operation: Operation
    items: list[str] = Field(min_length=1, max_length=500)
    language: str = "zh"
    tn_options: TNOptions = Field(default_factory=TNOptions)
    itn_options: ITNOptions = Field(default_factory=ITNOptions)
    num2words_options: Num2WordsOptions = Field(default_factory=Num2WordsOptions)


class BatchItemResponse(BaseModel):
    index: int
    input: str
    output: str | None = None
    error: str | None = None


class BatchResponse(BaseModel):
    operation: Operation
    language: str
    items: list[BatchItemResponse]
    success_count: int
    error_count: int
    metadata: dict[str, Any] = Field(default_factory=dict)
