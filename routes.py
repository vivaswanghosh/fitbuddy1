import json

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import ai_service
import crud
import schemas
from database import get_db

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/plans", response_model=schemas.PlanResponse)
def create_plan(plan_in: schemas.PlanRequest, db: Session = Depends(get_db)):
    user = crud.create_user(db, plan_in)
    plan_payload = ai_service.generate_plan(
        name=user.name,
        age=user.age,
        weight=user.weight,
        goal=user.goal,
        intensity=user.intensity,
    )
    tip = ai_service.get_tip(user.goal)
    plan = crud.create_plan(db, user, plan_payload, tip)
    return schemas.PlanResponse(
        id=plan.id,
        user_id=user.id,
        plan=plan_payload,
        tip=tip,
    )


@router.post("/feedback", response_model=schemas.PlanResponse)
def submit_feedback(feedback_in: schemas.FeedbackRequest, db: Session = Depends(get_db)):
    plan = crud.get_plan(db, feedback_in.plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    user = crud.get_user(db, plan.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    current_plan = json.loads(plan.plan_json)
    updated_plan = ai_service.regenerate_plan(
        current_plan=current_plan,
        feedback=feedback_in.feedback,
        goal=user.goal,
        intensity=user.intensity,
    )
    tip = ai_service.get_tip(user.goal)
    updated = crud.update_plan(db, plan, updated_plan, tip)
    crud.create_feedback(db, updated, feedback_in.feedback)
    return schemas.PlanResponse(
        id=updated.id,
        user_id=user.id,
        plan=updated_plan,
        tip=tip,
    )


@router.get("/tips", response_model=schemas.TipResponse)
def get_tip(goal: schemas.GoalType):
    return schemas.TipResponse(goal=goal, tip=ai_service.get_tip(goal))


@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/plans/{plan_id}", response_model=schemas.PlanResponse)
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = crud.get_plan(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    plan_payload = json.loads(plan.plan_json)
    return schemas.PlanResponse(
        id=plan.id,
        user_id=plan.user_id,
        plan=plan_payload,
        tip=plan.tip,
    )


@router.post("/ui/generate")
def ui_generate(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    weight: int = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    plan_in = schemas.PlanRequest(
        name=name,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity,
    )
    user = crud.create_user(db, plan_in)
    plan_payload = ai_service.generate_plan(
        name=user.name,
        age=user.age,
        weight=user.weight,
        goal=user.goal,
        intensity=user.intensity,
    )
    tip = ai_service.get_tip(user.goal)
    plan = crud.create_plan(db, user, plan_payload, tip)
    return RedirectResponse(url=f"/ui/plan/{plan.id}", status_code=303)


@router.post("/ui/feedback")
def ui_feedback(
    plan_id: int = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    plan = crud.get_plan(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    user = crud.get_user(db, plan.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    current_plan = json.loads(plan.plan_json)
    updated_plan = ai_service.regenerate_plan(
        current_plan=current_plan,
        feedback=feedback,
        goal=user.goal,
        intensity=user.intensity,
    )
    tip = ai_service.get_tip(user.goal)
    updated = crud.update_plan(db, plan, updated_plan, tip)
    crud.create_feedback(db, updated, feedback)
    return RedirectResponse(url=f"/ui/plan/{updated.id}", status_code=303)


@router.get("/ui/plan/{plan_id}", response_class=HTMLResponse)
def ui_plan(plan_id: int, request: Request, db: Session = Depends(get_db)):
    plan = crud.get_plan(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    plan_payload = json.loads(plan.plan_json)
    return templates.TemplateResponse(
        "plan.html",
        {
            "request": request,
            "plan": plan_payload,
            "tip": plan.tip,
            "plan_id": plan.id,
        },
    )
