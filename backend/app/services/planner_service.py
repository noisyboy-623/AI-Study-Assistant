from typing import List, Dict
from schemas.planner_schema import PlannerRequest, PlannerResponse, StudySlot, SubjectInput

def _round_robin_order(subjects: List[SubjectInput]) -> List[int]:
    """
    Return indices of subjects in priority-aware round-robin order:
    lower priority number gets picked first more often.
    """
    # Sort by priority (1 high -> 5 low), then by name for stability
    sorted_idx = sorted(range(len(subjects)),
                        key=lambda i: (subjects[i].priority, subjects[i].name.lower()))
    return sorted_idx

def generate_study_plan(req: PlannerRequest) -> PlannerResponse:
    # Remaining hours per subject
    remaining: Dict[int, int] = {i: s.hours for i, s in enumerate(req.subjects)}

    capacity = req.total_days * req.hours_per_day
    assigned = 0
    schedule: List[StudySlot] = []

    order = _round_robin_order(req.subjects)
    pick_ptr = 0

    for day in range(1, req.total_days + 1):
        day_left = req.hours_per_day

        while day_left > 0 and any(h > 0 for h in remaining.values()):
            # advance pointer to next subject that still has hours
            iter_count = 0
            while remaining[order[pick_ptr]] == 0 and iter_count < len(order):
                pick_ptr = (pick_ptr + 1) % len(order)
                iter_count += 1

            if all(h == 0 for h in remaining.values()):
                break

            idx = order[pick_ptr]
            # allocate up to max_session_hours, but not more than what's left in day or subject
            slot = min(req.max_session_hours, day_left, remaining[idx])

            schedule.append(StudySlot(
                day=day,
                subject=req.subjects[idx].name,
                duration=slot
            ))

            remaining[idx] -= slot
            day_left -= slot
            assigned += slot

            # move pointer for round-robin
            pick_ptr = (pick_ptr + 1) % len(order)

        if assigned >= capacity:
            break  # filled all capacity

    unallocated_total = sum(remaining.values())
    # If unallocated_total > 0, we didn’t have enough capacity

    return PlannerResponse(
        schedule=schedule,
        total_assigned_hours=assigned,
        total_capacity_hours=capacity,
        unallocated_hours=unallocated_total
    )
