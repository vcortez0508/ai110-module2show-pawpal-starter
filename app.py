import streamlit as st
from datetime import date
from pawpal_systems import Pet, Task, Schedule, Planner

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Initialize session state once ---
if "schedule" not in st.session_state:
    st.session_state.schedule = None

# --- Owner & Pet Setup ---
st.subheader("Owner & Pet Info")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Victor")
    available_time = st.number_input("Time available today (minutes)", min_value=10, max_value=480, value=120)
with col2:
    pet_name = st.text_input("Pet name", value="Biscuit")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed", value="Golden Retriever")
    age = st.number_input("Age", min_value=0, max_value=30, value=3)

if st.button("Save Owner & Pet"):
    pet = Pet(name=pet_name, species=species, breed=breed, age=age)
    st.session_state.schedule = Schedule(
        owner_name=owner_name,
        available_minutes_per_day=available_time,
        pet=pet,
        date=date.today(),
    )
    st.success(f"Saved! Planning for {pet_name} ({breed}) — {available_time}min budget.")

st.divider()

# --- Task Management ---
st.subheader("Add a Task")

if st.session_state.schedule is None:
    st.info("Save your owner & pet info above before adding tasks.")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        task_name = st.text_input("Task name", value="Morning Walk")
        category = st.selectbox("Category", ["walk", "feeding", "meds", "grooming", "enrichment"])
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30)
    with col3:
        priority = st.selectbox("Priority", ["high", "medium", "low"])
        recurring = st.selectbox("Recurring", ["daily", "weekly", "none"])

    if st.button("Add Task"):
        task = Task(
            name=task_name,
            category=category,
            duration_minutes=int(duration),
            priority=priority,
            recurring=recurring,
        )
        st.session_state.schedule.add_task(task)
        st.success(f"Added: {task_name} ({duration}min) [{priority}]")

    # --- Current Task List ---
    if st.session_state.schedule.tasks:
        st.markdown("### Current Tasks")
        task_data = [
            {
                "Task": t.name,
                "Category": t.category,
                "Duration": f"{t.duration_minutes}min",
                "Priority": t.priority.upper(),
                "Recurring": t.recurring,
                "Status": t.status,
            }
            for t in st.session_state.schedule.tasks
        ]
        st.table(task_data)
        total = sum(t.duration_minutes for t in st.session_state.schedule.tasks)
        remaining = st.session_state.schedule.available_minutes_per_day - total
        st.caption(f"Total: {total}min used | {remaining}min remaining")
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# --- Generate Schedule ---
st.subheader("Generate Schedule")

if st.button("Generate Schedule"):
    if st.session_state.schedule is None:
        st.warning("Save your owner & pet info first.")
    elif not st.session_state.schedule.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        planner = Planner(st.session_state.schedule)
        plan = planner.generate_plan()
        if not plan:
            st.warning("Planner returned no results — scheduling logic not implemented yet.")
        else:
            sched = st.session_state.schedule
            st.markdown(f"### Daily Plan for {sched.pet.name} ({sched.pet.breed})")
            st.caption(f"Owner: {sched.owner_name}  |  Date: {sched.date}  |  Budget: {sched.available_minutes_per_day}min")
            plan_data = [
                {
                    "Time": entry["time"],
                    "Task": entry["task"].name,
                    "Duration": f"{entry['task'].duration_minutes}min",
                    "Priority": entry["task"].priority.upper(),
                }
                for entry in plan
            ]
            st.table(plan_data)
            st.info(planner.explain_plan())
