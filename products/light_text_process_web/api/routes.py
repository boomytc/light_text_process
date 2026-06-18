from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar

from fastapi import APIRouter, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from light_text_process import TextProcessor
from light_text_process.capabilities import build_capabilities
from light_text_process.schemas import (
    BatchRequest,
    BatchResponse,
    ITNRequest,
    Num2WordsRequest,
    ProcessResponse,
    TNRequest,
)
from product_paths import TEMPLATES_DIR


router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
processor = TextProcessor()
T = TypeVar("T")


async def _run_processor(func: Callable[..., T], *args: Any) -> T:
    try:
        return await run_in_threadpool(func, *args)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        detail = str(exc) or exc.__class__.__name__
        raise HTTPException(status_code=500, detail=detail) from exc


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/api/v1/capabilities")
async def capabilities() -> dict[str, object]:
    return build_capabilities()


@router.post("/api/v1/tn", response_model=ProcessResponse)
async def normalize_text(request: TNRequest) -> ProcessResponse:
    return await _run_processor(processor.normalize_text, request.text, request.language, request.options)


@router.post("/api/v1/itn", response_model=ProcessResponse)
async def inverse_normalize_text(request: ITNRequest) -> ProcessResponse:
    return await _run_processor(processor.inverse_normalize_text, request.text, request.language, request.options)


@router.post("/api/v1/num2words", response_model=ProcessResponse)
async def number_to_words(request: Num2WordsRequest) -> ProcessResponse:
    return await _run_processor(processor.number_to_words, request.number, request.language, request.options)


@router.post("/api/v1/batch", response_model=BatchResponse)
async def batch_process(request: BatchRequest) -> BatchResponse:
    return await _run_processor(
        processor.batch,
        request.operation,
        request.items,
        request.language,
        request.tn_options,
        request.itn_options,
        request.num2words_options,
    )


@router.get("/partials/capabilities", response_class=HTMLResponse)
async def capability_partial(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="partials/capabilities.html",
        context={"capabilities": build_capabilities()},
    )
