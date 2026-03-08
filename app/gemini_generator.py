import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors

def _get_client() -> genai.Client:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")
    return genai.Client(api_key=api_key, http_options={"api_version": "v1"})


def _get_model_name() -> str:
    return os.getenv("GEMINI_MODEL", "models/gemini-2.0-flash")


def format_gemini_error(exc: Exception) -> str:
    message = str(exc)
    if "RESOURCE_EXHAUSTED" in message or "429" in message:
        if "limit: 0" in message:
            return (
                "Error: Gemini quota is not enabled for this API key/project "
                "(reported limit is 0). Enable billing or switch to a project/key "
                "with active Gemini quota."
            )
        return "Error: Gemini rate limit hit. Please retry in a few seconds."
    return f"Error: {message}"


def generate_workout_gemini(
    *, name: str, age: int, weight: int, goal: str, intensity: str
) -> str:
    client = _get_client()
    prompt = f"""
You are a professional fitness trainer.

Create a personalized, structured 7-day workout plan for someone with the goal of {goal}, and prefers {intensity} intensity workouts.

Each day must include:
- A warm-up (5-10 mins)
- Main workout (targeted exercises, sets & reps)
- Cooldown or recovery tip

Format:
Day 1:
Warm-up: ...
Main Workout: ...
Cooldown: ...
(Repeat for Day 2-7)

User details: name={name}, age={age}, weight={weight}.
"""
    try:
        response = client.models.generate_content(
            model=_get_model_name(),
            contents=prompt,
        )
        text = response.text.strip() if getattr(response, "text", None) else ""
        if not text:
            return "Error: Gemini returned an empty response."
        return text
    except (errors.ClientError, errors.ServerError) as exc:
        return format_gemini_error(exc)
