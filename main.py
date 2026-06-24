from pawpal_system import Owner, Pet, Task, Scheduler, Priority

# --- Setup ---
owner = Owner(id=1, name="Alex Rivera", email="alex@example.com", phone="555-1234")

buddy    = Pet(id=1, name="Buddy",    species="Dog",  breed="Golden Retriever", age=3, owner=owner)
whiskers = Pet(id=2, name="Whiskers", species="Cat",  breed="Tabby",            age=5, owner=owner)
goldie   = Pet(id=3, name="Goldie",   species="Fish", breed="Goldfish",          age=1, owner=owner)

owner.add_pet(buddy)
owner.add_pet(whiskers)
owner.add_pet(goldie)

# --- Tasks — two intentional overlaps to trigger conflict detection ---
# Overlap 1: Morning Walk starts 09:30 (30 min, ends 10:00); Feeding starts 09:45 (15 min, ends 10:00)
# Overlap 2: Grooming starts 07:00 (45 min, ends 07:45); Fish Feeding starts 07:30 (5 min, ends 07:35)
buddy.add_task(Task(id=1, name="Morning Walk",  duration=30, priority=Priority.HIGH,   frequency="daily",  scheduled_time="09:30"))
buddy.add_task(Task(id=2, name="Grooming",      duration=45, priority=Priority.MEDIUM, frequency="weekly", scheduled_time="07:00"))
buddy.add_task(Task(id=3, name="Training",      duration=25, priority=Priority.HIGH,   frequency="daily",  scheduled_time="11:15"))
buddy.add_task(Task(id=4, name="Evening Walk",  duration=30, priority=Priority.MEDIUM, frequency="daily",  scheduled_time="08:00"))

whiskers.add_task(Task(id=5, name="Feeding",    duration=15, priority=Priority.HIGH,   frequency="daily",  scheduled_time="09:45"))
whiskers.add_task(Task(id=6, name="Vet Checkup",duration=60, priority=Priority.LOW,    frequency="once",   scheduled_time="06:30"))
whiskers.add_task(Task(id=7, name="Playtime",   duration=20, priority=Priority.MEDIUM, frequency="daily",  scheduled_time="13:00"))

goldie.add_task(Task(id=8, name="Tank Cleaning",duration=20, priority=Priority.LOW,    frequency="weekly", scheduled_time="12:15"))
goldie.add_task(Task(id=9, name="Fish Feeding", duration=5,  priority=Priority.HIGH,   frequency="daily",  scheduled_time="07:30"))

# --- Populate schedule directly to preserve scrambled times ---
scheduler = Scheduler(owner=owner, available_minutes=240)
scheduler.schedule = [task for pet in owner.get_pets() for task in pet.tasks]

# Build a lookup: task id -> pet name
task_to_pet = {}
for pet in owner.get_pets():
    for task in pet.tasks:
        task_to_pet[task.id] = pet.name

# --- Print unsorted (as added) ---
print("=" * 52)
print("        SCHEDULE (unsorted / as added)")
print("=" * 52)
for task in scheduler.get_schedule():
    pet_label = task_to_pet.get(task.id, "?")
    print(f"  {task.scheduled_time}  {task.name:<20} {task.duration:>3} min"
          f"  [{task.priority.value:<6}]  {pet_label}")
print("=" * 52)

# --- Print sorted by scheduled_time ---
sorted_schedule = scheduler.sort_by_time()

print()
print("=" * 52)
print("        SCHEDULE (sorted by time)")
print("=" * 52)
for task in sorted_schedule:
    pet_label = task_to_pet.get(task.id, "?")
    print(f"  {task.scheduled_time}  {task.name:<20} {task.duration:>3} min"
          f"  [{task.priority.value:<6}]  {pet_label}")
print("=" * 52)

total_min = sum(t.duration for t in sorted_schedule)
print(f"  {len(sorted_schedule)} task(s)  |  {total_min} min total")
print("=" * 52)

# --- Conflict detection ---
conflicts = scheduler.detect_conflicts()
if conflicts:
    print()
    for msg in conflicts:
        print(msg)
else:
    print("\nNo scheduling conflicts detected.")
