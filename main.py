from datetime import date
from pawpal_systems import Pet, Task, Schedule, Planner

# --- Pets ---
biscuit = Pet(name="Biscuit", species="Dog", breed="Golden Retriever", age=3)
luna = Pet(name="Luna", species="Cat", breed="Siamese", age=5)

# --- Tasks for Biscuit (added out of time/priority order on purpose) ---
biscuit_schedule = Schedule(
    owner_name="Victor",
    available_minutes_per_day=120,
    pet=biscuit,
    date=date.today(),
)
biscuit_tasks = [
    Task(name="Flea Medicine", category="meds", duration_minutes=5, priority="medium", start_time="12:30", status="pending"),
    Task(name="Feeding", category="feeding", duration_minutes=10, priority="high", start_time="08:00", status="complete"),
    Task(name="Morning Walk", category="walk", duration_minutes=30, priority="high", start_time="07:15", status="complete"),
    Task(name="Vet Call", category="misc", duration_minutes=10, priority="medium", start_time="08:00", status="pending"),  # overlaps Feeding on purpose
]
for task in biscuit_tasks:
    warning = biscuit_schedule.add_task(task)
    if warning:
        print(warning)

# --- Tasks for Luna (added out of time/priority order on purpose) ---
luna_schedule = Schedule(
    owner_name="Victor",
    available_minutes_per_day=60,
    pet=luna,
    date=date.today(),
)
luna_tasks = [
    Task(name="Enrichment Play", category="enrichment", duration_minutes=15, priority="low", start_time="18:00", status="pending"),
    Task(name="Feeding", category="feeding", duration_minutes=10, priority="high", start_time="08:00", status="complete"),
    Task(name="Grooming", category="grooming", duration_minutes=20, priority="medium", start_time="17:00", status="pending"),
]
for task in luna_tasks:
    warning = luna_schedule.add_task(task)
    if warning:
        print(warning)

# --- Print Today's Schedule ---
def print_schedule(schedule: Schedule) -> None:
    header = f"  Daily Plan for {schedule.pet.name} ({schedule.pet.breed})  "
    sub = f"  Owner: {schedule.owner_name}  |  Date: {schedule.date}  "
    width = max(len(header), len(sub)) + 2
    print(f"\n+{'=' * width}+")
    print(f"|{header:<{width}}|")
    print(f"|{sub:<{width}}|")
    print(f"+{'=' * width}+")
    print(f"\n  {'#':<4} {'TIME':<7} {'TASK':<22} {'DURATION':<10} PRIORITY")
    print(f"  {'-' * (width - 2)}")
    total = 0
    start_hour, start_min = 8, 0
    for i, task in enumerate(schedule.tasks, start=1):
        time_str = f"{start_hour:02d}:{start_min:02d}"
        duration_str = f"{task.duration_minutes}min"
        print(f"  {i:<4} {time_str}  {task.name:<22} {duration_str:<10} {task.priority.upper()}")
        total += task.duration_minutes
        start_min += task.duration_minutes
        start_hour += start_min // 60
        start_min %= 60
    print(f"  {'-' * (width - 2)}")
    print(f"  {'Total:':<33} {total}min used  |  {schedule.available_minutes_per_day - total}min remaining\n")

print_schedule(biscuit_schedule)
print_schedule(luna_schedule)

# --- Demonstrate sort_by_time() and filter_by() ---
def print_task_list(title: str, tasks: list) -> None:
    print(f"\n  {title}")
    if not tasks:
        print("    (none)")
        return
    for task in tasks:
        print(f"    {task.start_time or '--:--':<6} {task.name:<22} [{task.priority}] status={task.status}")

for schedule in (biscuit_schedule, luna_schedule):
    planner = Planner(schedule)
    print(f"\n{'=' * 40}\n  {schedule.pet.name}: sorting & filtering demo\n{'=' * 40}")

    print_task_list("Tasks sorted by start_time:", planner.sort_by_time())
    print_task_list("Tasks filtered by status='pending':", planner.filter_by(status="pending"))
    print_task_list("Tasks filtered by status='complete':", planner.filter_by(status="complete"))
    print_task_list(f"Tasks filtered by pet_name='{schedule.pet.name}':", planner.filter_by(pet_name=schedule.pet.name))
    print_task_list("Tasks filtered by pet_name='NotARealPet':", planner.filter_by(pet_name="NotARealPet"))
