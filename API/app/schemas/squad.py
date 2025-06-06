from typing import List

from pydantic import BaseModel, Field


class SquadPlayer(BaseModel):
    name: str = Field(description="Player first name")
    surname: str = Field(description="Player surname")
    dob: str = Field(description="Player date of birth")
    position: str = Field(description="Player position")


class Squad(BaseModel):
    squad: List[SquadPlayer] = Field(description="Squad players")


class SquadFinderQuery(BaseModel):
    query: str = Field(description="User query")


class SquadFinderResponse(BaseModel):
    result: Squad = Field(description="Result with squad info")
    total_tokens_used: int = Field(description="Total tokens used", default=0)
    total_llm_call_time: float = Field(
        description="Total time taken for LLM call",
        default=0,
    )
