from dataclasses import dataclass, field
from datetime import date


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int

    def __str__(self) -> str:
        return f"{self.name} ({self.breed})"


@dataclass
class Task:
    name: str
    category: str
    duration_minutes: int
    priority: str  # "high", "medium", "low"
    recurring: str = "daily"  # "daily", "weekly", "none"
    notes: str = ""

    def __str__(self) -> str:
        return f"{self.name} ({self.duration_minutes} min) [{self.priority}]"

    def is_high_priority(self) -> bool:
        return self.priority == "high"


@dataclass
class Schedule:
    owner_name: str
    available_minutes_per_day: int
    pet: Pet
    date: date
    preferences: dict = field(default_factory=dict)
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def get_remaining_time(self) -> int:
        pass


class Planner:
    def __init__(self, schedule: Schedule):
        self.schedule = schedule

    def sort_tasks(self) -> list:
        pass

    def filter_tasks(self) -> list:
        pass

    def assign_time_slots(self) -> list:
        pass

    def generate_plan(self) -> list:
        pass

    def explain_plan(self) -> str:
        pass
