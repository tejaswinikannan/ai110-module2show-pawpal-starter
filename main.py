"""Quick CLI demo for PawPal+: build an owner, some pets and tasks, and print today's schedule."""

from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner.create_owner("Jordan")

mochi = Pet.add_pet("dog", "Mochi")
whiskers = Pet.add_pet("cat", "Whiskers")
owner.add_pet(mochi)
owner.add_pet(whiskers)

mochi.feed()
mochi.schedule_walk()
whiskers.tasks.append(Task.add_task("Litter box cleaning", duration_minutes=10, priority="medium"))
whiskers.tasks.append(Task.add_task("Grooming", duration_minutes=15, priority="low"))

scheduler = Scheduler()
todays_schedule = scheduler.build_daily_schedule(owner, start_time="08:00")

pet_name_by_task_id = {task.task_id: pet.name for pet in owner.pets for task in pet.tasks}

print(f"Today's Schedule for {owner.name}'s pets")
print("-" * 40)
for task in todays_schedule:
    pet_name = pet_name_by_task_id[task.task_id]
    print(f"{task.scheduled_time} - {pet_name}: {task.task_title} ({task.duration_minutes} min, {task.priority} priority)")
