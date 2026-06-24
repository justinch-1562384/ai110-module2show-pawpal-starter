from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Pet:
    id: int
    name: str
    species: str
    breed: str
    age: int
    owner: Owner  # direct reference instead of a bare owner_id int
    tasks: List[Task] = field(default_factory=list)

    def edit_pet_info(self, name: str, species: str, breed: str, age: int) -> None:
        """Update the pet's profile fields."""
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list if not already present."""
        if task not in self.tasks:
            self.tasks.append(task)

    def complete_task(self, task_id: int) -> None:
        """Mark the task with the given id as complete."""
        for task in self.tasks:
            if task.id == task_id:
                task.is_complete = True
                return


@dataclass
class Task:
    id: int
    name: str
    duration: int             # minutes
    priority: Priority
    frequency: str = "once"   # e.g. "once", "daily", "weekly"
    is_complete: bool = False
    scheduled_time: Optional[str] = None   # e.g. "08:00"; written by Scheduler.create_schedule()

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
        """Add a pet to this owner's list if not already present."""
        if pet not in self.pets:
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
        """Collect and return all tasks from every pet owned by the owner."""
        tasks = []
        for pet in self.owner.get_pets():
            tasks.extend(pet.tasks)
        return tasks

    def add_task(self, task: Task, pet: Pet) -> None:
        """Assign a task to a specific pet."""
        pet.add_task(task)

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
        """Sort incomplete tasks by priority and fit them within the available time budget."""
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        all_tasks = [t for t in self.get_all_tasks() if not t.is_complete]
        sorted_tasks = sorted(all_tasks, key=lambda t: priority_order[t.priority])
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
