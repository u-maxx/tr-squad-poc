from typing import Optional, Union

from app.config import settings
from app.utils.logging import logging
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)


class Gemini:
    client: genai.Client

    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize the Gemini client.

        Args:
            model_name: The name of the model to use.
        """
        self.model_name = model_name or settings.GEMINI_MODEL_NAME
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

    def generate_content(
        self,
        contents: Union[types.ContentListUnion, types.ContentListUnionDict],
        config: Optional[types.GenerateContentConfig] = None,
    ) -> types.GenerateContentResponse:
        """
        Generate content using the Gemini client.

        Args:
            contents: The content to generate.
            config: The configuration for the generation.
        """
        return self.client.models.generate_content(
            model=self.model_name,
            contents=contents,
            config=config,
        )
