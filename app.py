import streamlit as st
from pawpal_system import Pet, Owner, Task, Scheduler, Priority

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Session state ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "owner" not in st.session_state:
    st.session_state.owner = None

if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

if "task_counter" not in st.session_state:
    st.session_state.task_counter = 1

if "pet_counter" not in st.session_state:
    st.session_state.pet_counter = 1

# --- Owner & Pet Setup ---
st.subheader("Owner & Pet Setup")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name   = st.text_input("Pet name",   value="Mochi")
species    = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add Pet"):
    if st.session_state.owner is None:
        st.session_state.owner = Owner(id=1, name=owner_name, email="", phone="")
    pet = Pet(
        id=st.session_state.pet_counter,
        name=pet_name,
        species=species,
        breed="",
        age=0,
        owner=st.session_state.owner,
    )
    st.session_state.owner.add_pet(pet)
    st.session_state.pet_counter += 1
    st.success(f"Added {pet_name} to {owner_name}'s pets.")

if st.session_state.owner:
    pets = st.session_state.owner.get_pets()
    if pets:
        st.write("**Pets:**", ", ".join(p.name for p in pets))

st.divider()

# --- Tasks ---
st.subheader("Tasks")

if st.session_state.owner and st.session_state.owner.get_pets():
    pet_names         = [p.name for p in st.session_state.owner.get_pets()]
    selected_pet_name = st.selectbox("Assign task to", pet_names)
else:
    st.info("Add a pet above before adding tasks.")
    selected_pet_name = None

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    if selected_pet_name and st.session_state.owner:
        pet  = next(p for p in st.session_state.owner.get_pets() if p.name == selected_pet_name)
        task = Task(
            id=st.session_state.task_counter,
            name=task_title,
            duration=int(duration),
            priority=Priority[priority.upper()],
        )
        pet.add_task(task)
        st.session_state.task_counter += 1
        st.session_state.tasks.append(
            {"pet": selected_pet_name, "task": task_title, "duration (min)": int(duration), "priority": priority}
        )
        st.success(f"Added '{task_title}' to {selected_pet_name}.")
    else:
        st.warning("Add a pet first.")

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Schedule ---
st.subheader("Build Schedule")
available_minutes = st.number_input("Available minutes today", min_value=10, max_value=480, value=120)

if st.button("Generate schedule"):
    if st.session_state.owner and st.session_state.owner.get_all_tasks():
        scheduler = Scheduler(owner=st.session_state.owner, available_minutes=int(available_minutes))
        schedule  = scheduler.create_schedule()
        st.session_state.scheduler = scheduler

        if schedule:
            st.success("Schedule generated!")
            rows = []
            for task in schedule:
                pet_label = next(
                    (p.name for p in st.session_state.owner.get_pets() if task in p.tasks), "?"
                )
                rows.append({
                    "Time":           task.scheduled_time,
                    "Task":           task.name,
                    "Pet":            pet_label,
                    "Duration (min)": task.duration,
                    "Priority":       task.priority.value,
                })
            st.table(rows)
        else:
            st.warning("No tasks fit within the available time budget.")
    else:
        st.warning("Add at least one pet and task before generating a schedule.")
