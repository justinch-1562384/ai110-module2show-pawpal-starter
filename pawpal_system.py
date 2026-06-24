from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import Enum
from typing import List, Optional


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


def _to_minutes(time_str: str) -> int:
    """Convert "HH:MM" to an integer minute offset; shared by sort_by_time and detect_conflicts."""
    h, m = time_str.split(":")
    return int(h) * 60 + int(m)


@dataclass
class Pet:
    id: int
    name: str
    species: str
    breed: str
    age: int
    owner: Owner  # direct reference instead of a bare owner_id int
    tasks: List[Task] = field(default_factory=list)
    _next_id: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Seed _next_id so complete_task can assign recurring-task IDs in O(1) instead of scanning tasks each time."""
        self._next_id = max((t.id for t in self.tasks), default=0) + 1

    def edit_pet_info(self, name: str, species: str, breed: str, age: int) -> None:
        """Update the pet's profile fields."""
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age

    def add_task(self, task: Task) -> None:
        """Append a task if no existing task shares its id.

        Deduplicates by id rather than value equality — @dataclass __eq__ compares
        all fields, so a task updated in-place would not be caught by value comparison.
        """
        if not any(t.id == task.id for t in self.tasks):
            self.tasks.append(task)

    def complete_task(self, task_id: int) -> None:
        """Mark the task with the given id as complete; re-queue daily/weekly tasks.

        Uses _next_id counter (O(1)) instead of max(t.id for t in self.tasks) (O(n))
        to assign the new task's id.
        """
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task is None:
            return
        task.is_complete = True
        if task.frequency in ("daily", "weekly"):
            delta = timedelta(days=1) if task.frequency == "daily" else timedelta(weeks=1)
            self.tasks.append(Task(
                id=self._next_id,
                name=task.name,
                duration=task.duration,
                priority=task.priority,
                frequency=task.frequency,
                due_date=date.today() + delta,
            ))
            self._next_id += 1


@dataclass
class Task:
    id: int
    name: str
    duration: int             # minutes
    priority: Priority
    frequency: str = "once"   # e.g. "once", "daily", "weekly"
    is_complete: bool = False
    scheduled_time: Optional[str] = None   # e.g. "08:00"; written by Scheduler.create_schedule()
    due_date: Optional[date] = None        # set automatically for recurring tasks

    def edit_task(self, name: str, duration: int, priority: Priority) -> None:
        """Update the task's name, duration, and priority."""
        self.name = name
        self.duration = duration
        self.priority = priority

    def mark_complete(self) -> None:
        """Set the task's completion status to True."""
        self.is_complete = True


class Owner:
    def __init__(self, id: int, name: str, email: str, phone: str) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.pets: List[Pet] = []

    def edit_owner_info(self, name: str, email: str, phone: str) -> None:
        """Update the owner's contact information."""
        self.name = name
        self.email = email
        self.phone = phone

    def add_pet(self, pet: Pet) -> None:
        """Add a pet if no existing pet shares its id.

        Deduplicates by id rather than value equality — same reasoning as Pet.add_task.
        """
        if not any(p.id == pet.id for p in self.pets):
            self.pets.append(pet)

    def remove_pet(self, pet_id: int) -> None:
        """Remove the pet with the given id from this owner's list."""
        self.pets = [p for p in self.pets if p.id != pet_id]

    def get_pets(self) -> List[Pet]:
        """Return the list of all pets belonging to this owner."""
        return self.pets

    def get_pet_by_id(self, pet_id: int) -> Optional[Pet]:
        """Return the pet with the given id, or None if not found."""
        for p in self.pets:
            if p.id == pet_id:
                return p
        return None

    def get_all_tasks(self) -> List[Task]:
        """Return a flat list of every task across all owned pets."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks


class Scheduler:
    def __init__(self, owner: Owner, available_minutes: int) -> None:
        self.owner = owner
        self.available_minutes = available_minutes  # daily time budget for scheduling
        self.schedule: List[Task] = []

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across every owned pet; delegates to Owner to avoid duplicating traversal logic."""
        return self.owner.get_all_tasks()

    def remove_task(self, task_id: int) -> None:
        """Remove the task with the given id from the current schedule."""
        self.schedule = [t for t in self.schedule if t.id != task_id]

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Return the scheduled task with the given id, or None if not found."""
        for t in self.schedule:
            if t.id == task_id:
                return t
        return None

    def create_schedule(self) -> List[Task]:
        """Greedily pack incomplete tasks into the time budget, sorted by (priority, due_date).

        Greedy: tasks are sorted HIGH→LOW, with due_date as a tiebreaker within the same
        priority so more urgent tasks schedule first. Tasks are packed sequentially until
        the budget is exhausted. Note: this is a greedy 0/1 knapsack — not guaranteed optimal.
        """
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        all_tasks = [t for t in self.get_all_tasks() if not t.is_complete]
        sorted_tasks = sorted(all_tasks, key=lambda t: (priority_order[t.priority], t.due_date or date.max))
        minutes = 0
        result = []
        for task in sorted_tasks:
            if minutes + task.duration <= self.available_minutes:
                task.scheduled_time = f"{(minutes // 60):02d}:{(minutes % 60):02d}"
                result.append(task)
                minutes += task.duration
        self.schedule = result
        return self.schedule

    def get_schedule(self) -> List[Task]:
        """Return the most recently created schedule."""
        return self.schedule

    def sort_by_time(self) -> List[Task]:
        """Return the schedule sorted by scheduled_time ascending; unscheduled tasks sort last.

        Uses _to_minutes for numeric comparison rather than lexicographic string sort,
        which would break for hour values beyond two digits.
        """
        return sorted(self.schedule, key=lambda t: _to_minutes(t.scheduled_time) if t.scheduled_time else float("inf"))

    def detect_conflicts(self) -> List[str]:
        """Return warning messages for any tasks whose time intervals overlap.

        O(n log n) sort + O(n) adjacent-pair sweep instead of the naive O(n²) all-pairs check.
        Correctness: if A overlaps C (non-adjacent after sorting by start time), then B — which
        starts between A and C — must also overlap A, so the adjacent-pair sweep catches it.
        """
        scheduled = sorted(
            [t for t in self.schedule if t.scheduled_time],
            key=lambda t: _to_minutes(t.scheduled_time),
        )
        warnings = []
        for i in range(len(scheduled) - 1):
            a, b = scheduled[i], scheduled[i + 1]
            if _to_minutes(a.scheduled_time) + a.duration > _to_minutes(b.scheduled_time):
                warnings.append(
                    f"WARNING: '{a.name}' ({a.scheduled_time}, {a.duration} min) "
                    f"overlaps with '{b.name}' ({b.scheduled_time}, {b.duration} min)"
                )
        return warnings
