from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.models import Base
from app.routers import admin
from app.routers import comment
from app.routers import post
from app.routers import user
from app.routers.user import engine

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(admin.router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Madup Blog API",
        version="1.0.0",
        description=("백엔드 전환 포트폴리오용 API"),
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
