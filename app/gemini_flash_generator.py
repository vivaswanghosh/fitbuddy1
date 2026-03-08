import os

from google.genai import errors

from .gemini_generator import _get_client



def _get_flash_model() -> str:
    return os.getenv("GEMINI_FLASH_MODEL")



def generate_nutrition_tip_with_flash(goal: str) -> str:
    client = _get_client()
    prompt = (
        "Give one clear, helpful nutrition or recovery tip for someone focused on "
        f"'{goal}'. The tip should be practical, friendly, and easy to understand."
    )
    try:
        response = client.models.generate_content(
            model=_get_flash_model(),
            contents=prompt,
        )
        return response.text.strip() if getattr(response, "text", None) else ""
    except (errors.ClientError, errors.ServerError):
        return "Error: Unable to generate nutrition tip at this time."
