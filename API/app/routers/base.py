from app.config import settings
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    """
    Handles the root endpoint of the API.

    Returns:
        dict: A welcome message indicating the API is accessible.
    """
    return {"message": f"Welcome to {settings.APP_TITLE}"}
