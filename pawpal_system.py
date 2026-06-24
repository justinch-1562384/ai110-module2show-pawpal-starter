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

    def edit_pet_info(self, name: str, species: str, breed: str, age: int) -> None:
        pass


@dataclass
class Task:
    id: int
    name: str
    duration: int             # minutes
    priority: Priority
    scheduled_time: Optional[str] = None   # e.g. "08:00"; written by Scheduler.create_schedule()
    assigned_pets: List[Pet] = field(default_factory=list)
    assigned_owners: List[Owner] = field(default_factory=list)

    def edit_task(self, name: str, duration: int, priority: Priority) -> None:
        pass

    def assign_to_pet(self, pet: Pet) -> None:
        pass

    def assign_to_owner(self, owner: Owner) -> None:
        pass


class Owner:
    def __init__(self, id: int, name: str, email: str, phone: str) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.pets: List[Pet] = []

    def edit_owner_info(self, name: str, email: str, phone: str) -> None:
        pass

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet_id: int) -> None:
        pass

    def get_pets(self) -> List[Pet]:
        pass

    def get_pet_by_id(self, pet_id: int) -> Optional[Pet]:
        pass


class Scheduler:
    def __init__(self, owner: Owner, available_minutes: int) -> None:
        self.owner = owner
        self.available_minutes = available_minutes  # daily time budget for scheduling
        self.schedule: List[Task] = []

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task_id: int) -> None:
        pass

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        pass

    def create_schedule(self) -> List[Task]:
        pass

    def get_schedule(self) -> List[Task]:
        pass
