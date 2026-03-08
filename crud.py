import json
from datetime import datetime

from sqlalchemy.orm import Session

import models
import schemas


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
	user = models.User(
		name=user_in.name.strip(),
		age=user_in.age,
		weight=user_in.weight,
		goal=user_in.goal,
		intensity=user_in.intensity,
	)
	db.add(user)
	db.commit()
	db.refresh(user)
	return user


def get_user(db: Session, user_id: int) -> models.User | None:
	return db.query(models.User).filter(models.User.id == user_id).first()


def create_plan(
	db: Session, user: models.User, plan_payload: dict, tip: str | None
) -> models.Plan:
	plan = models.Plan(
		user_id=user.id,
		plan_json=json.dumps(plan_payload),
		tip=tip,
		created_at=datetime.utcnow(),
		updated_at=datetime.utcnow(),
	)
	db.add(plan)
	db.commit()
	db.refresh(plan)
	return plan


def update_plan(
	db: Session, plan: models.Plan, plan_payload: dict, tip: str | None
) -> models.Plan:
	plan.plan_json = json.dumps(plan_payload)
	plan.tip = tip
	plan.updated_at = datetime.utcnow()
	db.commit()
	db.refresh(plan)
	return plan


def get_plan(db: Session, plan_id: int) -> models.Plan | None:
	return db.query(models.Plan).filter(models.Plan.id == plan_id).first()


def get_latest_plan_for_user(db: Session, user_id: int) -> models.Plan | None:
	return (
		db.query(models.Plan)
		.filter(models.Plan.user_id == user_id)
		.order_by(models.Plan.created_at.desc())
		.first()
	)


def create_feedback(
	db: Session, plan: models.Plan, feedback_text: str
) -> models.Feedback:
	feedback = models.Feedback(plan_id=plan.id, comment=feedback_text)
	db.add(feedback)
	db.commit()
	db.refresh(feedback)
	return feedback
