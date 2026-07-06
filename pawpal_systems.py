from dataclasses import dataclass, field
from datetime import date


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int

    def __str__(self) -> str:
        """Return a human-readable name and breed string."""
        return f"{self.name} ({self.breed})"


@dataclass
class Task:
    name: str
    category: str
    duration_minutes: int
    priority: str  # "high", "medium", "low"
    recurring: str = "daily"  # "daily", "weekly", "none"
    notes: str = ""
    status: str = "pending"  # "pending" or "complete"

    def __str__(self) -> str:
        """Return a formatted task summary with duration and priority."""
        return f"{self.name} ({self.duration_minutes} min) [{self.priority}]"

    def is_high_priority(self) -> bool:
        """Return True if the task priority is high."""
        return self.priority == "high"

    def mark_complete(self) -> None:
        """Set the task status to complete."""
        self.status = "complete"


@dataclass
class Schedule:
    owner_name: str
    available_minutes_per_day: int
    pet: Pet
    date: date
    preferences: dict = field(default_factory=dict)
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to the schedule's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the schedule's task list."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_remaining_time(self) -> int:
        """Return the minutes remaining after subtracting all task durations from the daily budget."""
        return self.available_minutes_per_day - sum(t.duration_minutes for t in self.tasks)


class Planner:
    def __init__(self, schedule: Schedule):
        self.schedule = schedule

    def sort_tasks(self) -> list:
        """Return tasks sorted by priority (high → medium → low)."""
        order = {"high": 0, "medium": 1, "low": 2}
        return sorted(self.schedule.tasks, key=lambda t: order.get(t.priority, 3))

    def filter_tasks(self) -> list:
        """Return only the tasks that fit within the available time budget."""
        sorted_tasks = self.sort_tasks()
        budget = self.schedule.available_minutes_per_day
        selected, total = [], 0
        for task in sorted_tasks:
            if total + task.duration_minutes <= budget:
                selected.append(task)
                total += task.duration_minutes
        return selected

    def assign_time_slots(self) -> list:
        """Return tasks with a calculated start time based on order and duration."""
        filtered = self.filter_tasks()
        hour, minute = 8, 0
        slots = []
        for task in filtered:
            slots.append({"time": f"{hour:02d}:{minute:02d}", "task": task})
            minute += task.duration_minutes
            hour += minute // 60
            minute %= 60
        return slots

    def generate_plan(self) -> list:
        """Return the final ordered, time-slotted plan by running the full pipeline."""
        # pipeline: sort_tasks() → filter_tasks() → assign_time_slots()
        return self.assign_time_slots()

    def explain_plan(self) -> str:
        """Return a human-readable explanation of why tasks were ordered and filtered as they were."""
        filtered = self.filter_tasks()
        all_tasks = self.schedule.tasks
        dropped = [t for t in all_tasks if t not in filtered]
        total = sum(t.duration_minutes for t in filtered)
        lines = [
            f"Tasks were sorted by priority (high → medium → low) and scheduled starting at 08:00.",
            f"{len(filtered)} of {len(all_tasks)} tasks fit within the {self.schedule.available_minutes_per_day}min budget ({total}min used).",
        ]
        if dropped:
            names = ", ".join(t.name for t in dropped)
            lines.append(f"Dropped due to time constraints: {names}.")
        return " ".join(lines)
