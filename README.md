# FitBuddy – AI Fitness Plan Generator

FitBuddy is a FastAPI web app that uses Google Gemini models to create a personalized 7-day workout plan and a goal-based nutrition or recovery tip. It stores user details, generated plans, and feedback in SQLite. The project provides both REST API endpoints and a clean HTML interface.

## Features

- Generate a 7-day workout plan from user inputs (user_id, goal, intensity)
- Regenerate plans based on feedback ("more cardio", "add rest days")
- Goal-aligned nutrition or recovery tips
- SQLite persistence for users, plans, and feedback
- API endpoints plus a browser-based UI

## Tech Stack

- FastAPI
- SQLite + SQLAlchemy
- Pydantic
- Google Gemini (google-genai)
- Jinja2 templates

## Setup

1) Create and activate a virtual environment.
2) Install dependencies:

```
pip install -r requirements.txt
```

3) Create a .env file (or set environment variables) with your Gemini API key:

```
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-1.5-pro-002
GEMINI_FLASH_MODEL=gemini-1.5-flash-002
```

4) Run the app:

```
uvicorn app.main:app --reload
```

5) Open the UI:

```
http://127.0.0.1:8000/
```

## API Endpoints

### Generate Plan

POST /plans

Request body:

```
{
  "user_id": 101,
  "name": "Alex",
  "age": 24,
  "weight": 68,
  "goal": "weight loss",
  "intensity": "medium"
}
```

Response body (example):

```
{
  "id": 1,
  "user_id": 1,
  "plan": "Day 1:\nWarm-up: ...\nMain Workout: ...\nCooldown: ...\n...",
  "tip": "Aim for a small calorie deficit and include protein at every meal."
}
```

### Submit Feedback (Regenerate Plan)

POST /feedback

Request body:

```
{
  "user_id": 101,
  "feedback": "Add more cardio on Day 2"
}
```

### Get Plan by ID

GET /plans/{plan_id}

### Get User by ID

GET /users/{user_id}

## UI Routes

- GET /: main form page
- POST /generate-workout: create a plan from form input
- POST /submit-feedback: send feedback and regenerate
- GET /view-all-users: admin view of all users

## Notes

- Plans are stored as plain text in SQLite and returned as formatted text.
- You can change the model via `GEMINI_MODEL` and `GEMINI_FLASH_MODEL` in .env if your account supports different models.
- You can adjust prompts in app/gemini_generator.py and app/updated_plan.py.




