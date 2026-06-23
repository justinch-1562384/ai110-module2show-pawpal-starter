from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class Pet:
    id: int
    name: str
    species: str
    breed: str
    age: int
    owner_id: int

    def add_pet_info(self, name: str, species: str, breed: str, age: int) -> None:
        pass

    def edit_pet_info(self, name: str, species: str, breed: str, age: int) -> None:
        pass


@dataclass
class Task:
    id: int
    name: str
    duration: int        # minutes
    priority: str        # "low", "medium", "high"
    assigned_pets: List[Pet] = field(default_factory=list)
    assigned_owners: List[Owner] = field(default_factory=list)

    def add_task(self, name: str, duration: int, priority: str) -> None:
        pass

    def edit_task(self, name: str, duration: int, priority: str) -> None:
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

    def add_owner_info(self, name: str, email: str, phone: str) -> None:
        pass

    def edit_owner_info(self, name: str, email: str, phone: str) -> None:
        pass

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_pets(self) -> List[Pet]:
        pass


class Scheduler:
    def __init__(self) -> None:
        self.schedule: List[Task] = []

    def add_task(self, task: Task) -> None:
        pass

    def create_schedule(self) -> List[Task]:
        pass

    def get_schedule(self) -> List[Task]:
        pass
