from typing import Annotated

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

from backend.app.api.controllers.auth import router as auth_router
from backend.app.api.controllers.games import router as games_router
from backend.app.api.controllers.offers import router as offers_router
from backend.app.api.controllers.genres import router as genres_router
from backend.app.api.controllers.platforms import router as platforms_router
from backend.app.api.controllers.stores import router as stores_router
from backend.app.api.controllers.publishers import router as publishers_router
from backend.app.api.controllers.users import router as users_router

app = FastAPI()

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Hello World"}

@app.get("/docs", include_in_schema=False)
async def get_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

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

    uvicorn.run(
        app="backend.app.main:app",
        log_level="debug",
        reload=True
    )


