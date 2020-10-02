from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from routers import auth, sched
from utils.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(sched.router, prefix="/sched", tags=["sched"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="1.0.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
