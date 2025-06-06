import uvicorn
from app.config import settings
from app.routers.base import router as base_router
from app.routers.squad_finder import router as squad_router
from app.utils.logging import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    """
    Creates and configures the FastAPI application instance.

    This function initializes the FastAPI app with metadata, configures CORS middleware
    using allowed origins and regex patterns, and includes the main API routers.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    application = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
    )

    allow_origins = []
    allow_origins.extend(settings.PUBLIC_END_USER_UI_URL)

    allow_origin_regex = f"https://{settings.VERCEL_PROJECT_PREFIX}-.*-{settings.VERCEL_PROJECT_SUFFIX}\.vercel\.app"  # noqa
    application.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_origin_regex=allow_origin_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    application.include_router(base_router)
    application.include_router(squad_router)

    return application


# Create the FastAPI application
app = create_application()

if __name__ == "__main__":
    # Debugging purposes https://fastapi.tiangolo.com/tutorial/debugging/#call-uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
