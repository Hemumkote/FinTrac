from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.common import APIResponse, ErrorDetail


async def validation_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """
    Catches pydantic validation errors
    Reformates them into standard APIRespponse shape
    """
    assert isinstance(exc, RequestValidationError)

    errors = []
    for err in exc.errors():
        field = str(err["loc"][-1]) if err["loc"] else "unknown"
        errors.append(ErrorDetail(field=field, message=err["msg"]))

    response = APIResponse.error(message="Validation failed", status=422, errors=errors)
    return JSONResponse(status_code=422, content=response.model_dump())


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Catches all the HTTPException (400,401,403,404,409...)
    """
    http_exc = exc if isinstance(exc, HTTPException) else HTTPException(status_code=500)
    response = APIResponse.error(
        message=str(http_exc.detail), status=http_exc.status_code
    )
    return JSONResponse(status_code=http_exc.status_code, content=response.model_dump())


async def value_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catches the value error"""
    assert isinstance(exc, ValueError)
    response = APIResponse.error(message=str(exc), status=422)
    return JSONResponse(status_code=422, content=response.model_dump())


async def starlette_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """
    Catches Starlette's base HTTPException (e.g. 404 route not found, 405 method not allowed)
    that are NOT caught by the FastAPI HTTPException handler.
    """
    starlette_exc = (
        exc if isinstance(exc, StarletteHTTPException) else StarletteHTTPException(500)
    )
    response = APIResponse.error(
        message=str(starlette_exc.detail), status=starlette_exc.status_code
    )
    return JSONResponse(
        status_code=starlette_exc.status_code, content=response.model_dump()
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catches the unexcepted errors"""
    response = APIResponse.error(message="Internal error occured", status=500)
    return JSONResponse(status_code=500, content=response.model_dump())
