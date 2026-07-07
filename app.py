import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner.create_owner(owner_name)
owner = st.session_state.owner

scheduler = Scheduler()

st.divider()

st.subheader("Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    submitted_pet = st.form_submit_button("Add pet")

if submitted_pet:
    pet = Pet.add_pet(species, pet_name)
    owner.add_pet(pet)

if owner.pets:
    st.markdown("### Pets & Tasks")
    for pet in owner.pets:
        with st.expander(f"{pet.name} ({pet.pet_type})", expanded=True):
            col1, col2 = st.columns(2)
            if col1.button("Feed", key=f"feed_{pet.name}"):
                pet.feed()
            if col2.button("Schedule walk", key=f"walk_{pet.name}"):
                pet.schedule_walk()

            with st.form(f"add_task_form_{pet.name}", clear_on_submit=True):
                task_title = st.text_input("Task title", value="Meds", key=f"title_{pet.name}")
                duration = st.number_input(
                    "Duration (minutes)", min_value=1, max_value=240, value=20, key=f"duration_{pet.name}"
                )
                priority = st.selectbox(
                    "Priority", ["low", "medium", "high"], index=2, key=f"priority_{pet.name}"
                )
                submitted_task = st.form_submit_button("Add task")

            if submitted_task:
                task = Task.add_task(task_title, duration_minutes=int(duration), priority=priority)
                pet.tasks.append(task)

            if pet.tasks:
                pending_tasks = scheduler.sort_by_time(scheduler.filter_by_status(pet.tasks, completed=False))
                completed_tasks = scheduler.filter_by_status(pet.tasks, completed=True)

                if pending_tasks:
                    st.table([task.view_tasks()[0] for task in pending_tasks])
                if completed_tasks:
                    st.success(f"✅ {len(completed_tasks)} task(s) completed for {pet.name}.")
                if not pending_tasks and not completed_tasks:
                    st.info("No tasks yet for this pet.")
            else:
                st.info("No tasks yet for this pet.")
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Prioritizes every pet's tasks and assigns start times.")

if st.button("Generate schedule"):
    todays_schedule = scheduler.sort_by_time(scheduler.build_daily_schedule(owner))

    if todays_schedule:
        pet_name_by_task_id = {task.task_id: pet.name for pet in owner.pets for task in pet.tasks}
        st.success(f"✅ Scheduled {len(todays_schedule)} task(s) for {owner.name}, in chronological order.")
        st.table(
            [
                {
                    "time": task.scheduled_time,
                    "pet": pet_name_by_task_id[task.task_id],
                    "task": task.task_title,
                    "duration_minutes": task.duration_minutes,
                    "priority": task.priority,
                }
                for task in todays_schedule
            ]
        )

        conflicts = scheduler.detect_conflicts(owner)
        if conflicts:
            for warning in conflicts:
                st.warning(f"⚠️ {warning}")
        else:
            st.success("No scheduling conflicts detected.")
    else:
        st.info("No tasks to schedule yet. Add a pet and some tasks above.")
