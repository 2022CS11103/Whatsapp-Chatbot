"""Application entrypoint. Run with: uvicorn app.main:app --reload"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import auth_router, business_router, faq_router, knowledge_base_router
from app.config.logging_config import configure_logging
from app.config.settings import get_settings
from app.middleware.error_handler_middleware import register_exception_handlers
from app.middleware.logging_middleware import RequestLoggingMiddleware


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestLoggingMiddleware)

    register_exception_handlers(app)

    app.include_router(auth_router.router, prefix=settings.API_V1_PREFIX)
    app.include_router(business_router.router, prefix=settings.API_V1_PREFIX)
    app.include_router(faq_router.router, prefix=settings.API_V1_PREFIX)
    app.include_router(knowledge_base_router.router, prefix=settings.API_V1_PREFIX)

    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
