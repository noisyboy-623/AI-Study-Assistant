from fastapi import APIRouter, HTTPException
from schemas.planner_schema import PlannerRequest, PlannerResponse
from services.planner_service import generate_study_plan

router = APIRouter()

@router.post("/planner", response_model=PlannerResponse, tags=["Study Planner"])
def create_plan(request: PlannerRequest):
    if not request.subjects:
        raise HTTPException(status_code=400, detail="At least one subject is required.")
    return generate_study_plan(request)
