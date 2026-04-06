# app/main.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from app.api.controllers.auth import router as auth_router
from app.api.controllers.games import router as games_router
from app.api.controllers.offers import router as offers_router
from app.api.controllers.genres import router as genres_router
from app.api.controllers.platforms import router as platforms_router
from app.api.controllers.stores import router as stores_router
from app.api.controllers.publishers import router as publishers_router
from app.api.controllers.users import router as users_router
from app.exception_handlers import (
    app_http_exception_handler,
    request_validation_handler,
    unhandled_exception_handler,
)
from app.exceptions import AppHTTPException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppHTTPException, app_http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(games_router)
app.include_router(offers_router)
app.include_router(stores_router)
app.include_router(platforms_router)
app.include_router(publishers_router)
app.include_router(genres_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", log_level="debug", port=8080)