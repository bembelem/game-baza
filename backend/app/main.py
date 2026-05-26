import sys
from pathlib import Path

from starlette.responses import FileResponse

sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from app.api.controllers.auth import router as auth_router
from app.api.controllers.games import router as games_router
from app.api.controllers.catalogs import (
    router_developers,
    router_genres,
    router_platforms,
    router_publishers,
    router_stores,
)
from app.api.controllers.users import router as users_router


from app.exception_handlers import (
    app_http_exception_handler,
    request_validation_handler,
    unhandled_exception_handler,
)
from app.exceptions import AppHTTPException
from app.logging_config import setup_logging
from app.middleware.request_id import RequestIdMiddleware

SPEC_PATH = Path(__file__).parent.parent.parent / "docs" / "api" / "openapi.yaml"

setup_logging(level="INFO")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)
app.add_middleware(RequestIdMiddleware)


@app.get("/openapi.yaml", include_in_schema=False)
async def get_openapi_spec():
    return FileResponse(SPEC_PATH, media_type="application/yaml")


app.add_exception_handler(AppHTTPException, app_http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(games_router)
app.include_router(router_stores)
app.include_router(router_platforms)
app.include_router(router_publishers)
app.include_router(router_developers)
app.include_router(router_genres)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", log_level="debug", port=8000)
