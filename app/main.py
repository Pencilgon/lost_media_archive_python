from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import Base, engine
from .routers import media, collections, attempts


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(
    title="Lost Media Archive API",
    description="REST API for managing lost media and recovery attempts.",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(collections.router)
app.include_router(media.router)
app.include_router(attempts.router)


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}