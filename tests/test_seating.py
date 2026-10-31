import itertools

from app.features.seating import SeatingRequest, plan_seating


def test_no_same_class_neighbours():
    students = {f"s{i}": ("10A" if i % 2 else "10B") for i in range(8)}
    plan = plan_seating(SeatingRequest(students=students, rows=2, seats_per_row=4))
    for row in plan.seats:
        for left, right in itertools.pairwise(row):
            if left and right:
                assert students[left] != students[right]
    placed = [s for row in plan.seats for s in row if s]
    assert sorted(placed) == sorted(students)
