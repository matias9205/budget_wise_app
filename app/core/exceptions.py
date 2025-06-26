from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

class ExceptionsHandlers:
    def add_exception_handlers(self, app: FastAPI):
        @app.exception_handler(StarletteHTTPException)
        async def http_exception_handler(request: Request, exc: StarletteHTTPException):
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc: RequestValidationError):
            errors = exc.errors()
            # Optional: strip out context that causes serialization issues
            for error in errors:
                if "ctx" in error:
                    ctx = error["ctx"]
                    error["ctx"] = {k: str(v) for k, v in ctx.items()}
            return JSONResponse(status_code=422, content={"detail": errors[0]["msg"]})