import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_task_status():
    task = Task.add_task("Feeding", duration_minutes=10, priority="high")

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet.add_pet("dog", "Mochi")

    assert len(pet.tasks) == 0

    pet.feed()

    assert len(pet.tasks) == 1


# --- Sorting correctness ---


def test_sort_by_time_returns_chronological_order():
    scheduler = Scheduler()
    late = Task.add_task("Walk", recurrence=None)
    late.scheduled_time = "18:00"
    early = Task.add_task("Feeding")
    early.scheduled_time = "07:00"
    midday = Task.add_task("Medication")
    midday.scheduled_time = "12:30"

    ordered = scheduler.sort_by_time([late, early, midday])

    assert [t.task_title for t in ordered] == ["Feeding", "Medication", "Walk"]


def test_sort_by_time_places_unscheduled_tasks_last():
    scheduler = Scheduler()
    scheduled = Task.add_task("Feeding")
    scheduled.scheduled_time = "09:00"
    unscheduled = Task.add_task("Walk")  # scheduled_time defaults to None

    ordered = scheduler.sort_by_time([unscheduled, scheduled])

    assert ordered == [scheduled, unscheduled]


def test_sort_by_time_empty_pet_returns_empty_list():
    pet = Pet.add_pet("cat", "Nimbus")

    assert Scheduler().sort_by_time(pet.tasks) == []


def test_sort_by_time_is_stable_for_identical_times():
    scheduler = Scheduler()
    first = Task.add_task("Feeding")
    first.scheduled_time = "09:00"
    second = Task.add_task("Medication")
    second.scheduled_time = "09:00"

    ordered = scheduler.sort_by_time([first, second])

    assert ordered == [first, second]


# --- Recurrence logic ---


def test_completing_daily_task_creates_task_for_following_day():
    pet = Pet.add_pet("dog", "Mochi")
    task = Task.add_task("Feeding", recurrence="daily", due_date=date(2026, 7, 6))
    pet.tasks.append(task)

    next_task = pet.complete_task(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == date(2026, 7, 7)
    assert next_task.completed is False
    assert next_task.task_title == "Feeding"
    assert next_task in pet.tasks


def test_completing_weekly_task_creates_task_for_following_week():
    pet = Pet.add_pet("dog", "Mochi")
    task = Task.add_task("Grooming", recurrence="weekly", due_date=date(2026, 7, 6))
    pet.tasks.append(task)

    next_task = pet.complete_task(task)

    assert next_task.due_date == date(2026, 7, 13)


def test_completing_task_without_due_date_defaults_to_today():
    task = Task.add_task("Feeding", recurrence="daily", due_date=None)

    next_task = task.next_occurrence()

    assert next_task.due_date == date.today() + timedelta(days=1)


def test_completing_non_recurring_task_creates_no_next_task():
    pet = Pet.add_pet("cat", "Nimbus")
    task = Task.add_task("One-time vet visit", recurrence=None)
    pet.tasks.append(task)

    next_task = pet.complete_task(task)

    assert next_task is None
    assert len(pet.tasks) == 1


# --- Conflict detection ---


def test_detect_conflicts_flags_duplicate_times():
    scheduler = Scheduler()
    owner = Owner.create_owner("Alex")
    pet_a = owner.add_pet(Pet.add_pet("dog", "Mochi"))
    pet_b = owner.add_pet(Pet.add_pet("cat", "Nimbus"))

    task_a = Task.add_task("Feeding")
    task_a.scheduled_time = "08:00"
    pet_a.tasks.append(task_a)

    task_b = Task.add_task("Walk")
    task_b.scheduled_time = "08:00"
    pet_b.tasks.append(task_b)

    warnings = scheduler.detect_conflicts(owner)

    assert len(warnings) == 1
    assert "08:00" in warnings[0]
    assert "Mochi" in warnings[0] and "Nimbus" in warnings[0]


def test_detect_conflicts_no_warning_for_unique_times():
    scheduler = Scheduler()
    owner = Owner.create_owner("Alex")
    pet = owner.add_pet(Pet.add_pet("dog", "Mochi"))

    task_a = Task.add_task("Feeding")
    task_a.scheduled_time = "08:00"
    pet.tasks.append(task_a)

    task_b = Task.add_task("Walk")
    task_b.scheduled_time = "09:00"
    pet.tasks.append(task_b)

    assert scheduler.detect_conflicts(owner) == []


def test_detect_conflicts_ignores_unscheduled_tasks():
    scheduler = Scheduler()
    owner = Owner.create_owner("Alex")
    pet = owner.add_pet(Pet.add_pet("dog", "Mochi"))

    pet.tasks.append(Task.add_task("Feeding"))  # scheduled_time is None
    pet.tasks.append(Task.add_task("Walk"))  # scheduled_time is None

    assert scheduler.detect_conflicts(owner) == []


def test_detect_conflicts_for_owner_with_no_pets_returns_no_warnings():
    scheduler = Scheduler()
    owner = Owner.create_owner("Alex")

    assert scheduler.detect_conflicts(owner) == []


def test_detect_conflicts_for_pet_with_no_tasks_returns_no_warnings():
    scheduler = Scheduler()
    owner = Owner.create_owner("Alex")
    owner.add_pet(Pet.add_pet("dog", "Mochi"))

    assert scheduler.detect_conflicts(owner) == []
