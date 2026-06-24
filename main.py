from pawpal_system import Owner, Pet, Task, Scheduler, Priority

# --- Setup ---
owner = Owner(id=1, name="Alex Rivera", email="alex@example.com", phone="555-1234")

buddy    = Pet(id=1, name="Buddy",    species="Dog", breed="Golden Retriever", age=3, owner=owner)
whiskers = Pet(id=2, name="Whiskers", species="Cat", breed="Tabby",            age=5, owner=owner)

owner.add_pet(buddy)
owner.add_pet(whiskers)

# --- Tasks (different durations) ---
buddy.add_task(Task(id=1, name="Morning Walk",    duration=30, priority=Priority.HIGH,   frequency="daily"))
buddy.add_task(Task(id=2, name="Grooming",        duration=45, priority=Priority.MEDIUM, frequency="weekly"))
whiskers.add_task(Task(id=3, name="Feeding",      duration=15, priority=Priority.HIGH,   frequency="daily"))
whiskers.add_task(Task(id=4, name="Vet Checkup",  duration=60, priority=Priority.LOW,    frequency="once"))

# --- Schedule (2-hour daily budget) ---
scheduler = Scheduler(owner=owner, available_minutes=120)
schedule  = scheduler.create_schedule()

# Build a lookup: task id -> pet name
task_to_pet = {}
for pet in owner.get_pets():
    for task in pet.tasks:
        task_to_pet[task.id] = pet.name

# --- Print ---
print("=" * 48)
print("             TODAY'S SCHEDULE")
print("=" * 48)
for task in schedule:
    pet_label = task_to_pet.get(task.id, "?")
    print(f"  {task.scheduled_time}  {task.name:<20} {task.duration:>3} min"
          f"  [{task.priority.value:<6}]  {pet_label}")
print("=" * 48)

total_min = sum(t.duration for t in schedule)
print(f"  {len(schedule)} task(s) scheduled  |  {total_min} / {scheduler.available_minutes} min used")
print("=" * 48)
