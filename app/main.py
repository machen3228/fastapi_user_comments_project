from fastapi import FastAPI
import uvicorn

from app.api.routers import main_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_title,
    description=settings.description)

app.include_router(main_router)

if __name__ == '__main__':
    uvicorn.run("app.main:app", reload=True)
