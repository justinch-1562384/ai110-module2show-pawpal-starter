import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Owner, Pet, Task, Priority


def make_owner():
    return Owner(id=1, name="Test Owner", email="test@example.com", phone="555-0000")


def make_pet(owner):
    return Pet(id=1, name="Buddy", species="Dog", breed="Labrador", age=2, owner=owner)


def make_task(task_id=1, duration=30):
    return Task(id=task_id, name="Walk", duration=duration, priority=Priority.MEDIUM)


def test_mark_complete_sets_is_complete():
    task = make_task()
    assert task.is_complete is False
    task.mark_complete()
    assert task.is_complete is True


def test_add_task_increases_pet_task_count():
    owner = make_owner()
    pet = make_pet(owner)
    assert len(pet.tasks) == 0
    pet.add_task(make_task(task_id=1))
    pet.add_task(make_task(task_id=2))
    assert len(pet.tasks) == 2
