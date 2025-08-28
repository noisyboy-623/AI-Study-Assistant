from pydantic import BaseModel, Field, conint
from typing import List, Optional

class SubjectInput(BaseModel):
    name: str = Field(..., min_length=1)
    hours: conint(strict=True, ge=1)   # total hours needed for this subject
    priority: conint(strict=True, ge=1, le=5) = 3  # 1 = highest

class PlannerRequest(BaseModel):
    subjects: List[SubjectInput]
    total_days: conint(strict=True, ge=1)
    hours_per_day: conint(strict=True, ge=1)
    max_session_hours: conint(strict=True, ge=1, le=4) = 2  # cap per session

class StudySlot(BaseModel):
    day: int                   # 1-based
    subject: str
    duration: int              # hours in this session

class PlannerResponse(BaseModel):
    schedule: List[StudySlot]
    total_assigned_hours: int
    total_capacity_hours: int
    unallocated_hours: Optional[int] = 0   # > 0 means not enough capacity
