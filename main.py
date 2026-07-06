from datetime import date
from pawpal_systems import Pet, Task, Schedule

# --- Pets ---
biscuit = Pet(name="Biscuit", species="Dog", breed="Golden Retriever", age=3)
luna = Pet(name="Luna", species="Cat", breed="Siamese", age=5)

# --- Tasks for Biscuit ---
biscuit_schedule = Schedule(
    owner_name="Victor",
    available_minutes_per_day=120,
    pet=biscuit,
    date=date.today(),
)
biscuit_schedule.tasks = [
    Task(name="Morning Walk", category="walk", duration_minutes=30, priority="high"),
    Task(name="Feeding", category="feeding", duration_minutes=10, priority="high"),
    Task(name="Flea Medicine", category="meds", duration_minutes=5, priority="medium"),
]

# --- Tasks for Luna ---
luna_schedule = Schedule(
    owner_name="Victor",
    available_minutes_per_day=60,
    pet=luna,
    date=date.today(),
)
luna_schedule.tasks = [
    Task(name="Feeding", category="feeding", duration_minutes=10, priority="high"),
    Task(name="Grooming", category="grooming", duration_minutes=20, priority="medium"),
    Task(name="Enrichment Play", category="enrichment", duration_minutes=15, priority="low"),
]

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
