from dataclasses import dataclass, field, replace
from datetime import date, timedelta


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
    start_time: str = ""  # "HH:MM", zero-padded, optional
    due_date: date = field(default_factory=date.today)

    def __str__(self) -> str:
        """Return a formatted task summary with duration and priority."""
        return f"{self.name} ({self.duration_minutes} min) [{self.priority}]"

    def is_high_priority(self) -> bool:
        """Return True if the task priority is high."""
        return self.priority == "high"

    def next_occurrence(self) -> "Task | None":
        """Return a new pending Task instance for the next due date, or None if not recurring."""
        if self.recurring == "daily":
            delta = timedelta(days=1)
        elif self.recurring == "weekly":
            delta = timedelta(weeks=1)
        else:
            return None
        return replace(self, status="pending", due_date=self.due_date + delta)

    def mark_complete(self) -> "Task | None":
        """Set the task status to complete and return the next occurrence, if recurring."""
        self.status = "complete"
        return self.next_occurrence()


@dataclass
class Schedule:
    owner_name: str
    available_minutes_per_day: int
    pet: Pet
    date: date
    preferences: dict = field(default_factory=dict)
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> str | None:
        """Append a task to the schedule's task list. Return a warning string if it overlaps an existing task, else None."""
        warning = self.check_conflict(task)
        self.tasks.append(task)
        return warning

    def check_conflict(self, task: Task) -> str | None:
        """Return a lightweight warning message if task's time range overlaps an existing task, else None."""
        if not task.start_time:
            return None
        start, end = Planner._time_range(task)
        for existing in self.tasks:
            if not existing.start_time or existing is task:
                continue
            ex_start, ex_end = Planner._time_range(existing)
            if start < ex_end and ex_start < end:
                return (
                    f"Warning: '{task.name}' ({task.start_time}) overlaps "
                    f"'{existing.name}' ({existing.start_time}) for {self.pet.name}."
                )
        return None

    def remove_task(self, task: Task) -> None:
        """Remove a task from the schedule's task list."""
        if task in self.tasks:
            self.tasks.remove(task)

    def complete_task(self, task: Task) -> Task | None:
        """Mark a task complete and add its next occurrence to the schedule, if recurring."""
        next_task = task.mark_complete()
        if next_task is not None:
            self.add_task(next_task)
        return next_task

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

    def sort_by_time(self) -> list:
        """Return tasks sorted by their start_time attribute (HH:MM strings)."""
        return sorted(self.schedule.tasks, key=lambda t: t.start_time)

    def filter_by(self, status: str = None, pet_name: str = None) -> list:
        """Return tasks matching the given status and/or pet name, if provided."""
        tasks = self.schedule.tasks
        if status is not None:
            tasks = [t for t in tasks if t.status == status]
        if pet_name is not None:
            tasks = [t for t in tasks if self.schedule.pet.name == pet_name]
        return tasks

    @staticmethod
    def _time_range(task: "Task") -> tuple[int, int]:
        """Return (start_minute, end_minute) since midnight for a task's start_time and duration."""
        hour, minute = map(int, task.start_time.split(":"))
        start = hour * 60 + minute
        return start, start + task.duration_minutes

    def find_conflicts(self, other_schedules: list = None) -> list:
        """Return pairs of tasks whose [start, start+duration) ranges overlap, within this schedule and against any other_schedules given."""
        others = [(self.schedule, t) for t in self.schedule.tasks if t.start_time]
        for other_schedule in other_schedules or []:
            others.extend((other_schedule, t) for t in other_schedule.tasks if t.start_time)

        conflicts = []
        for i, (sched_a, task_a) in enumerate(others):
            start_a, end_a = self._time_range(task_a)
            for sched_b, task_b in others[i + 1:]:
                start_b, end_b = self._time_range(task_b)
                if start_a < end_b and start_b < end_a:
                    conflicts.append((sched_a.pet.name, task_a, sched_b.pet.name, task_b))
        return conflicts

    def explain_conflicts(self, other_schedules: list = None) -> str:
        """Return a human-readable summary of any scheduling conflicts found."""
        conflicts = self.find_conflicts(other_schedules)
        if not conflicts:
            return "No scheduling conflicts found."
        lines = [f"{len(conflicts)} scheduling conflict(s) found:"]
        for pet_a, task_a, pet_b, task_b in conflicts:
            start_a, end_a = self._time_range(task_a)
            start_b, end_b = self._time_range(task_b)
            fmt = lambda m: f"{m // 60:02d}:{m % 60:02d}"
            lines.append(
                f"  {pet_a}'s '{task_a.name}' ({fmt(start_a)}-{fmt(end_a)}) overlaps "
                f"{pet_b}'s '{task_b.name}' ({fmt(start_b)}-{fmt(end_b)})"
            )
        return "\n".join(lines)

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
