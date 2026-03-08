# FitBuddy – AI Fitness Plan Generator

FitBuddy is a FastAPI web app that uses Google Gemini models to create a personalized 7-day workout plan and a goal-based nutrition or recovery tip. It stores user details, generated plans, and feedback in SQLite. The project provides both REST API endpoints and a clean HTML interface.

## Features

- Generate a 7-day workout plan from user inputs (goal and intensity)
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

## Project Structure

- ai_service.py: Gemini integration and prompt handling
- crud.py: database helper functions
- database.py: SQLAlchemy engine, session, and Base
- main.py: app startup and router wiring
- models.py: ORM models (User, Plan, Feedback)
- routes.py: all API and UI routes
- schemas.py: Pydantic request and response models
- templates/: HTML templates
- static/: CSS styles
- requirements.txt: dependencies

## Setup

1) Create and activate a virtual environment.
2) Install dependencies:

```
pip install -r requirements.txt
```

3) Create a .env file (or set environment variables) with your Gemini API key:

```
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-1.5-flash-002
```

4) Run the app:

```
uvicorn main:app --reload
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
  "plan": {
    "goal": "weight loss",
    "intensity": "medium",
    "days": [
      {
        "day": "Day 1",
        "focus": "Full body",
        "duration_minutes": 40,
        "exercises": [
          {"name": "Squats", "sets": 3, "reps": 12}
        ]
      }
    ]
  },
  "tip": "Aim for a small calorie deficit and include protein at every meal."
}
```

### Submit Feedback (Regenerate Plan)

POST /feedback

Request body:

```
{
  "plan_id": 1,
  "feedback": "Add more cardio on Day 2"
}
```

### Get Plan by ID

GET /plans/{plan_id}

### Get User by ID

GET /users/{user_id}

### Get Tip

GET /tips?goal=muscle%20gain

## UI Routes

- GET /: main form page
- POST /ui/generate: create a plan from form input
- GET /ui/plan/{plan_id}: view the plan
- POST /ui/feedback: send feedback and regenerate

## Notes

- Plans are stored as JSON strings in SQLite and returned as structured JSON.
- Gemini output is expected as strict JSON. If parsing fails, a safe fallback plan is used.
- You can change the model via `GEMINI_MODEL` in .env if your account supports a different model.
- You can adjust the prompts or model in ai_service.py.

## Common Issues

- GEMINI_API_KEY missing: set it in .env or your environment.
- Form data error: install python-multipart with `pip install python-multipart`.
- Gemini returns invalid JSON: the app falls back to a default plan.
- SQLite database file is created automatically as fitbuddy.db.

## License

This project is for educational use in the Smart Bridge course.
