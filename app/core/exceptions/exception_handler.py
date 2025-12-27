from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def register_exception_handler(
    app: FastAPI, base_exception: type, default_error: str = "error"
):
    """
    Registers a generic exception handler for all subclasses of `base_exception`.
    Automatically reads `status_code`, `error`, `message`, and optional `field` from the exception class.
    """

    @app.exception_handler(base_exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        content = {
            "error": getattr(exc, "error", default_error),
            "message": getattr(exc, "message", str(exc)),
        }

        field = getattr(exc, "field", None)
        if field:
            content["field"] = field

        return JSONResponse(
            status_code=getattr(exc, "status_code", 500),
            content=content,
        )
