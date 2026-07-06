from datetime import date, timedelta
from pawpal_systems import Task, Pet, Schedule, Planner


def make_pet(name="Biscuit"):
    return Pet(name=name, species="Dog", breed="Golden Retriever", age=3)


def make_schedule(pet=None, available_minutes_per_day=120):
    return Schedule(
        owner_name="Victor",
        available_minutes_per_day=available_minutes_per_day,
        pet=pet or make_pet(),
        date=date.today(),
    )


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


# --- Sorting correctness ---

def test_sort_by_time_returns_chronological_order():
    schedule = make_schedule()
    late = Task(name="Dinner", category="feeding", duration_minutes=20, priority="medium", start_time="18:00")
    early = Task(name="Breakfast", category="feeding", duration_minutes=15, priority="medium", start_time="07:00")
    mid = Task(name="Walk", category="walk", duration_minutes=30, priority="medium", start_time="12:30")
    schedule.add_task(late)
    schedule.add_task(early)
    schedule.add_task(mid)

    ordered = Planner(schedule).sort_by_time()

    assert [t.name for t in ordered] == ["Breakfast", "Walk", "Dinner"]


def test_sort_by_time_places_untimed_tasks_first():
    schedule = make_schedule()
    timed = Task(name="Walk", category="walk", duration_minutes=30, priority="medium", start_time="09:00")
    untimed = Task(name="Grooming", category="grooming", duration_minutes=15, priority="low")
    schedule.add_task(timed)
    schedule.add_task(untimed)

    ordered = Planner(schedule).sort_by_time()

    assert ordered[0].name == "Grooming"
    assert ordered[1].name == "Walk"


# --- Recurring logic ---

def test_mark_complete_on_daily_task_creates_next_day_task():
    today = date.today()
    task = Task(name="Morning Walk", category="walk", duration_minutes=30, priority="high",
                recurring="daily", due_date=today)

    next_task = task.mark_complete()

    assert task.status == "complete"
    assert next_task is not None
    assert next_task.status == "pending"
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.name == "Morning Walk"


def test_mark_complete_on_weekly_task_creates_next_week_task():
    today = date.today()
    task = Task(name="Bath", category="grooming", duration_minutes=20, priority="low",
                recurring="weekly", due_date=today)

    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task.due_date == today + timedelta(weeks=1)


def test_mark_complete_on_non_recurring_task_returns_none():
    task = Task(name="Vet Visit", category="health", duration_minutes=60, priority="high", recurring="none")

    next_task = task.mark_complete()

    assert task.status == "complete"
    assert next_task is None


def test_complete_task_appends_next_occurrence_to_schedule():
    schedule = make_schedule()
    task = Task(name="Morning Walk", category="walk", duration_minutes=30, priority="high", recurring="daily")
    schedule.add_task(task)

    next_task = schedule.complete_task(task)

    assert next_task in schedule.tasks
    assert len(schedule.tasks) == 2


# --- Conflict detection ---

def test_add_task_flags_duplicate_start_time():
    schedule = make_schedule()
    schedule.add_task(Task(name="Walk", category="walk", duration_minutes=30, priority="high", start_time="09:00"))

    warning = schedule.add_task(
        Task(name="Vet Call", category="health", duration_minutes=15, priority="medium", start_time="09:00")
    )

    assert warning is not None
    assert "overlaps" in warning


def test_add_task_flags_overlapping_but_not_identical_time():
    schedule = make_schedule()
    schedule.add_task(Task(name="Walk", category="walk", duration_minutes=30, priority="high", start_time="09:00"))

    warning = schedule.add_task(
        Task(name="Grooming", category="grooming", duration_minutes=30, priority="medium", start_time="09:15")
    )

    assert warning is not None


def test_add_task_does_not_flag_back_to_back_tasks():
    schedule = make_schedule()
    schedule.add_task(Task(name="Walk", category="walk", duration_minutes=30, priority="high", start_time="09:00"))

    warning = schedule.add_task(
        Task(name="Feeding", category="feeding", duration_minutes=15, priority="medium", start_time="09:30")
    )

    assert warning is None


def test_add_task_without_start_time_never_conflicts():
    schedule = make_schedule()
    schedule.add_task(Task(name="Walk", category="walk", duration_minutes=30, priority="high", start_time="09:00"))

    warning = schedule.add_task(
        Task(name="Grooming", category="grooming", duration_minutes=15, priority="low")
    )

    assert warning is None


# --- Edge cases ---

def test_empty_schedule_has_no_tasks_and_full_budget():
    schedule = make_schedule(available_minutes_per_day=120)
    planner = Planner(schedule)

    assert schedule.get_remaining_time() == 120
    assert planner.sort_tasks() == []
    assert planner.filter_tasks() == []
    assert planner.assign_time_slots() == []


def test_filter_tasks_includes_task_that_exactly_fits_budget():
    schedule = make_schedule(available_minutes_per_day=30)
    schedule.add_task(Task(name="Walk", category="walk", duration_minutes=30, priority="high"))

    filtered = Planner(schedule).filter_tasks()

    assert len(filtered) == 1
    assert schedule.get_remaining_time() == 0
