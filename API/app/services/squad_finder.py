import json
import re
import time

from app.ai.gemini import Gemini
from app.ai.system_instructions import get_squad_finder_instructions
from app.config import settings
from app.schemas.squad import Squad, SquadFinderQuery, SquadFinderResponse
from app.utils.logging import logging
from fastapi import HTTPException
from google.genai import types

logger = logging.getLogger(__name__)


class SquadFinder(Gemini):

    def find_squad_by_query(self, query: SquadFinderQuery) -> SquadFinderResponse:
        """
        Find the squad of a Premier League team upon a natural language request.

        Args:
            query: The query to find the squad by.

        Returns:
            SquadFinderResponse: The squad finder response with squad information and debugging information.
        """
        custom_user_query = f"User Query: {query}"

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=custom_user_query),
                ],
            ),
        ]

        if settings.GEMINI_GROUNDING_ENABLED:
            tools = [
                types.Tool(google_search=types.GoogleSearch()),
            ]
        else:
            tools = []

        generate_content_config = types.GenerateContentConfig(
            temperature=settings.GEMINI_TEMPERATURE,
            top_p=settings.GEMINI_TOP_P,
            max_output_tokens=settings.GEMINI_MAX_TOKENS,
            tools=tools,
            response_mime_type="text/plain",
            system_instruction=[get_squad_finder_instructions()],
        )

        try:
            start_time = time.monotonic()
            response = self.generate_content(
                contents=contents,
                config=generate_content_config,
            )
            end_time = time.monotonic()
            total_llm_call_time = end_time - start_time
            logger.info(
                f"TIME: Total for squad finder LLM call {total_llm_call_time:.2f}: seconds",
            )

            total_tokens_used = response.usage_metadata.total_token_count
            logger.info(
                f"TOKENS: Total Gemini API tokens used: {total_tokens_used}",
            )

            result_from_gemini = response.text
            # Remove code block markers
            cleaned_result_from_gemini = re.sub(
                r"^```json\n|```$",
                "",
                result_from_gemini.strip(),
                flags=re.MULTILINE,
            )

            # Extract the first JSON array from the string
            json_array_match = re.search(
                r"\[.*\]",
                cleaned_result_from_gemini,
                re.DOTALL,
            )
            if not json_array_match:
                logger.error(
                    f"No JSON array found in Gemini response: {cleaned_result_from_gemini}",
                )
                raise HTTPException(
                    status_code=500,
                    detail=f"No JSON array found in Gemini response: {cleaned_result_from_gemini}",
                )

            json_array_str = json_array_match.group(0)

            # Parse JSON with error handling
            try:
                parsed_result = json.loads(json_array_str)
            except json.JSONDecodeError as e:
                logger.error(
                    f"Failed to parse JSON from Gemini response: {e}\nResponse: {json_array_str}",
                )
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to parse JSON from Gemini response: {e}\nResponse: {json_array_str}",
                )

            result = SquadFinderResponse(
                result=Squad(squad=parsed_result),
                total_tokens_used=total_tokens_used,
                total_elapsed_time=total_llm_call_time,
            )

            return result
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            raise HTTPException(status_code=500, detail=f"Gemini API call failed: {e}")
