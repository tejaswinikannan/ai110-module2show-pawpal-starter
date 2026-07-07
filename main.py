"""Quick CLI demo for PawPal+: build an owner, some pets and tasks, and print today's schedule."""

from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner.create_owner("Jordan")

mochi = Pet.add_pet("dog", "Mochi")
whiskers = Pet.add_pet("cat", "Whiskers")
owner.add_pet(mochi)
owner.add_pet(whiskers)

# Tasks are added out of priority/time order on purpose, to prove the
# sorting and filtering logic doesn't depend on insertion order.
whiskers.tasks.append(Task.add_task("Grooming", duration_minutes=15, priority="low"))
mochi.schedule_walk()
whiskers.tasks.append(Task.add_task("Litter box cleaning", duration_minutes=10, priority="medium"))
mochi.feed()

# Mark one task already done so filter_by_status has something to exclude.
whiskers.tasks[0].mark_complete()

scheduler = Scheduler()
pet_name_by_task_id = {task.task_id: pet.name for pet in owner.pets for task in pet.tasks}


def print_tasks(title: str, tasks: list) -> None:
    print(title)
    print("-" * 40)
    if not tasks:
        print("(none)")
    for task in tasks:
        pet_name = pet_name_by_task_id[task.task_id]
        time_label = task.scheduled_time or "--:--"
        status = "done" if task.completed else "pending"
        print(f"{time_label} - {pet_name}: {task.task_title} ({task.duration_minutes} min, {task.priority} priority, {status})")
    print()


todays_schedule = scheduler.build_daily_schedule(owner, start_time="08:00")
print_tasks(f"Today's Schedule for {owner.name}'s pets", todays_schedule)

# Scramble the already-scheduled tasks, then prove sort_by_time restores order.
scrambled = list(reversed(todays_schedule))
print_tasks("Schedule scrambled out of order", scrambled)
print_tasks("Schedule restored with sort_by_time()", scheduler.sort_by_time(scrambled))

# Filtering demos, run against every task (including the completed one that
# build_daily_schedule skips).
all_tasks = scheduler.view_daily_routines(owner)
print_tasks("Pending tasks only (filter_by_status)", scheduler.filter_by_status(all_tasks, completed=False))
print_tasks("Completed tasks only (filter_by_status)", scheduler.filter_by_status(all_tasks, completed=True))
print_tasks("Whiskers' tasks only (filter_by_pet)", scheduler.filter_by_pet(owner, "Whiskers"))
