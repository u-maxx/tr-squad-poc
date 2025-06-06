from app.schemas.squad import SquadFinderQuery, SquadFinderResponse
from app.services.squad_finder import SquadFinder
from fastapi import APIRouter, Body, HTTPException

router = APIRouter(prefix="/api/v2")


@router.post("/squad-finder", responses={500: {"description": "Internal Server Error"}})
async def squad_finder(
    query: SquadFinderQuery = Body(...),
) -> SquadFinderResponse:
    """
    Find the squad of a Premier League team upon a natural language request
    """
    try:
        squad_finder = SquadFinder()
        result = squad_finder.find_squad_by_query(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
