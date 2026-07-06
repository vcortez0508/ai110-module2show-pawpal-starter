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
        pass

    def get_remaining_time(self) -> int:
        """Return the minutes remaining after subtracting all task durations from the daily budget."""
        pass


class Planner:
    def __init__(self, schedule: Schedule):
        self.schedule = schedule

    def sort_tasks(self) -> list:
        """Return tasks sorted by priority (high → medium → low)."""
        pass

    def filter_tasks(self) -> list:
        """Return only the tasks that fit within the available time budget."""
        pass

    def assign_time_slots(self) -> list:
        """Return tasks with a calculated start time based on order and duration."""
        pass

    def generate_plan(self) -> list:
        """Return the final ordered, time-slotted plan by running the full pipeline."""
        # pipeline: sort_tasks() → filter_tasks() → assign_time_slots()
        pass

    def explain_plan(self) -> str:
        """Return a human-readable explanation of why tasks were ordered and filtered as they were."""
        pass
