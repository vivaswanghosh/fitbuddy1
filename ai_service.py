import json
import os
from typing import Any, Dict

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
	return os.getenv("GEMINI_MODEL", "gemini-1.5-flash-002")


def _fallback_plan(goal: str, intensity: str) -> Dict[str, Any]:
	return {
		"goal": goal,
		"intensity": intensity,
		"days": [
			{
				"day": "Day 1",
				"focus": "Full body",
				"duration_minutes": 40,
				"exercises": [
					{"name": "Squats", "sets": 3, "reps": 12},
					{"name": "Push-ups", "sets": 3, "reps": 10},
					{"name": "Plank", "duration_minutes": 2},
				],
			},
			{
				"day": "Day 2",
				"focus": "Cardio",
				"duration_minutes": 30,
				"exercises": [
					{"name": "Brisk walk", "duration_minutes": 20},
					{"name": "Cycling", "duration_minutes": 10},
				],
			},
			{
				"day": "Day 3",
				"focus": "Rest",
				"duration_minutes": 0,
				"exercises": [{"name": "Recovery stretch", "duration_minutes": 10}],
			},
			{
				"day": "Day 4",
				"focus": "Upper body",
				"duration_minutes": 40,
				"exercises": [
					{"name": "Dumbbell rows", "sets": 3, "reps": 12},
					{"name": "Shoulder press", "sets": 3, "reps": 10},
				],
			},
			{
				"day": "Day 5",
				"focus": "Lower body",
				"duration_minutes": 40,
				"exercises": [
					{"name": "Lunges", "sets": 3, "reps": 12},
					{"name": "Glute bridges", "sets": 3, "reps": 15},
				],
			},
			{
				"day": "Day 6",
				"focus": "Cardio + Core",
				"duration_minutes": 35,
				"exercises": [
					{"name": "Jogging", "duration_minutes": 20},
					{"name": "Bicycle crunches", "sets": 3, "reps": 15},
				],
			},
			{
				"day": "Day 7",
				"focus": "Rest",
				"duration_minutes": 0,
				"exercises": [{"name": "Light yoga", "duration_minutes": 15}],
			},
		],
	}


def generate_plan(
	*, name: str, age: int, weight: int, goal: str, intensity: str
) -> Dict[str, Any]:
	client = _get_client()
	prompt = (
		"You are a fitness coach. Create a 7-day workout plan as strict JSON with this format: "
		'{"goal":"...","intensity":"...","days":[{"day":"Day 1","focus":"...",'
		'"duration_minutes":40,"exercises":[{"name":"...","sets":3,"reps":12,'
		'"duration_minutes":10,"notes":"..."}]}]}. '
		"Use exactly 7 days. If a rest day, set duration_minutes to 0 and include a recovery exercise. "
		"No markdown, no extra keys. User details: "
		f"name={name}, age={age}, weight={weight}, goal={goal}, intensity={intensity}."
	)
	try:
		response = client.models.generate_content(
			model=_get_model_name(),
			contents=prompt,
		)
		text = response.text.strip() if getattr(response, "text", None) else ""
		return json.loads(text)
	except (json.JSONDecodeError, errors.ClientError, errors.ServerError):
		return _fallback_plan(goal, intensity)


def regenerate_plan(
	*, current_plan: Dict[str, Any], feedback: str, goal: str, intensity: str
) -> Dict[str, Any]:
	client = _get_client()
	prompt = (
		"You are a fitness coach. Update the given 7-day plan based on feedback. "
		"Return strict JSON using the same format as the original plan, no markdown, no extra keys. "
		f"Goal={goal}, intensity={intensity}. Feedback: {feedback}. "
		f"Current plan JSON: {json.dumps(current_plan)}"
	)
	try:
		response = client.models.generate_content(
			model=_get_model_name(),
			contents=prompt,
		)
		text = response.text.strip() if getattr(response, "text", None) else ""
		return json.loads(text)
	except (json.JSONDecodeError, errors.ClientError, errors.ServerError):
		return current_plan


def get_tip(goal: str) -> str:
	tips = {
		"weight loss": "Aim for a small calorie deficit and include protein at every meal.",
		"muscle gain": "Include 20-30g protein within an hour after training.",
		"general wellness": "Prioritize sleep and hydrate regularly throughout the day.",
	}
	return tips.get(goal, "Stay consistent with balanced meals and recovery.")
