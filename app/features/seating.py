"""Exam seating with OR-Tools CP-SAT: no two students of the same class sit side by side."""

from ortools.sat.python import cp_model
from pydantic import BaseModel


class SeatingRequest(BaseModel):
    students: dict[str, str]  # student_id -> class_section
    rows: int
    seats_per_row: int


class SeatingPlan(BaseModel):
    seats: list[list[str | None]]  # rows x seats, student_id or empty


def plan_seating(req: SeatingRequest, time_limit_s: float = 5.0) -> SeatingPlan:
    ids = list(req.students)
    seats = [(r, c) for r in range(req.rows) for c in range(req.seats_per_row)]
    if len(ids) > len(seats):
        raise ValueError("More students than seats")

    m = cp_model.CpModel()
    x = {(s, p): m.new_bool_var(f"x_{s}_{p}") for s in range(len(ids)) for p in range(len(seats))}
    for s in range(len(ids)):
        m.add_exactly_one(x[s, p] for p in range(len(seats)))
    for p in range(len(seats)):
        m.add_at_most_one(x[s, p] for s in range(len(ids)))

    index = {seat: i for i, seat in enumerate(seats)}
    for a in range(len(ids)):
        for b in range(a + 1, len(ids)):
            if req.students[ids[a]] != req.students[ids[b]]:
                continue
            for (r, c), p in index.items():
                q = index.get((r, c + 1))
                if q is None:
                    continue
                m.add_bool_or([x[a, p].Not(), x[b, q].Not()])
                m.add_bool_or([x[b, p].Not(), x[a, q].Not()])

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_s
    if solver.solve(m) not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise ValueError("No seating satisfies the rules; add rooms or relax constraints")

    grid: list[list[str | None]] = [[None] * req.seats_per_row for _ in range(req.rows)]
    for s, sid in enumerate(ids):
        for p, (r, c) in enumerate(seats):
            if solver.value(x[s, p]):
                grid[r][c] = sid
    return SeatingPlan(seats=grid)
