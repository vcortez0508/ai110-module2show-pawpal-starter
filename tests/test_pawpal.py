from datetime import date
from pawpal_systems import Task, Pet, Schedule


def test_mark_complete_changes_status():
    task = Task(name="Morning Walk", category="walk", duration_minutes=30, priority="high")
    assert task.status == "pending"
    task.mark_complete()
    assert task.status == "complete"


def test_mark_complete_does_not_affect_other_fields():
    task = Task(name="Feeding", category="feeding", duration_minutes=10, priority="high")
    task.mark_complete()
    assert task.name == "Feeding"
    assert task.duration_minutes == 10
    assert task.priority == "high"


def test_add_task_increases_task_count():
    pet = Pet(name="Biscuit", species="Dog", breed="Golden Retriever", age=3)
    schedule = Schedule(owner_name="Victor", available_minutes_per_day=120, pet=pet, date=date.today())
    assert len(schedule.tasks) == 0
    schedule.add_task(Task(name="Morning Walk", category="walk", duration_minutes=30, priority="high"))
    assert len(schedule.tasks) == 1
    schedule.add_task(Task(name="Feeding", category="feeding", duration_minutes=10, priority="high"))
    assert len(schedule.tasks) == 2
