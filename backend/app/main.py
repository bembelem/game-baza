import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI

from app.api.controllers.auth import router as auth_router
from app.api.controllers.games import router as games_router
from app.api.controllers.offers import router as offers_router
from app.api.controllers.genres import router as genres_router
from app.api.controllers.platforms import router as platforms_router
from app.api.controllers.stores import router as stores_router
from app.api.controllers.publishers import router as publishers_router
from app.api.controllers.users import router as users_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(games_router)
app.include_router(offers_router)
app.include_router(stores_router)
app.include_router(platforms_router)
app.include_router(publishers_router)
app.include_router(genres_router)


from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc: RequestValidationError):
    error = exc.errors()[0]
    field = error["loc"][-1]
    msg = error["msg"]
    return JSONResponse(status_code=422, content={"detail": f"{field}: {msg}"})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="app.main:app",
        log_level="debug",
        reload=True
    )
