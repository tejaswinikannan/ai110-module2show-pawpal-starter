# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule for Jordan's pets
----------------------------------------
08:00 - Mochi: Feeding (10 min, high priority)
08:10 - Whiskers: Litter box cleaning (10 min, medium priority)
08:20 - Mochi: Walk (30 min, medium priority)
08:50 - Whiskers: Grooming (15 min, low priority)
```

## 🧪 Testing PawPal+

Run the suite from the project root:

```bash
python -m pytest -v
```

The suite in [`test/test_pawpal.py`](test/test_pawpal.py) covers:

- **Sorting correctness** — `Scheduler.sort_by_time()` orders tasks chronologically, pushes unscheduled (`scheduled_time=None`) tasks to the end, returns `[]` for a pet with no tasks, and preserves relative order when two tasks share the same time.
- **Recurrence logic** — completing a `"daily"` or `"weekly"` task produces a new, incomplete `Task` due exactly one interval later (and appends it to the pet's task list); a task with no `due_date` falls back to today; a non-recurring task produces no follow-up.
- **Conflict detection** — `Scheduler.detect_conflicts()` flags two tasks (even across different pets) scheduled at the exact same time, stays silent when times differ, and doesn't misfire on two unscheduled tasks or an owner/pet with no tasks at all.

Sample test output:

```
============================= test session starts =============================
platform win32 -- Python 3.10.10, pytest-9.0.3, pluggy-1.6.0 -- C:\Users\dteja\AppData\Local\Programs\Python\Python310\python.exe
cachedir: .pytest_cache
rootdir: E:\projects\codepath\ai110-module2show-pawpal-starter
plugins: anyio-4.3.0, time-machine-2.14.0
collecting ... collected 15 items

test/test_pawpal.py::test_mark_complete_changes_task_status PASSED       [  6%]
test/test_pawpal.py::test_adding_task_increases_pet_task_count PASSED    [ 13%]
test/test_pawpal.py::test_sort_by_time_returns_chronological_order PASSED [ 20%]
test/test_pawpal.py::test_sort_by_time_places_unscheduled_tasks_last PASSED [ 26%]
test/test_pawpal.py::test_sort_by_time_empty_pet_returns_empty_list PASSED [ 33%]
test/test_pawpal.py::test_sort_by_time_is_stable_for_identical_times PASSED [ 40%]
test/test_pawpal.py::test_completing_daily_task_creates_task_for_following_day PASSED [ 46%]
test/test_pawpal.py::test_completing_weekly_task_creates_task_for_following_week PASSED [ 53%]
test/test_pawpal.py::test_completing_task_without_due_date_defaults_to_today PASSED [ 60%]
test/test_pawpal.py::test_completing_non_recurring_task_creates_no_next_task PASSED [ 66%]
test/test_pawpal.py::test_detect_conflicts_flags_duplicate_times PASSED  [ 73%]
test/test_pawpal.py::test_detect_conflicts_no_warning_for_unique_times PASSED [ 80%]
test/test_pawpal.py::test_detect_conflicts_ignores_unscheduled_tasks PASSED [ 86%]
test/test_pawpal.py::test_detect_conflicts_for_owner_with_no_pets_returns_no_warnings PASSED [ 93%]
test/test_pawpal.py::test_detect_conflicts_for_pet_with_no_tasks_returns_no_warnings PASSED [100%]

============================= 15 passed in 0.05s ==============================
```

**Confidence Level: ⭐⭐⭐⭐☆ (4/5)**

All 15 tests pass, and the core scheduling behaviors (sorting, recurrence, conflict detection) are covered for both the happy path and their key edge cases. One star is held back because `detect_conflicts()` only flags tasks with an *identical* `scheduled_time` string — it won't catch overlapping-but-not-identical time windows (e.g., a 30-minute walk at 08:00 overlapping a feeding at 08:15), which isn't tested or handled yet.

## 📐 Smarter Scheduling

| Feature            | Method(s)                      | Notes |
|------------------- |--------------------------------|-------|
| Priority sorting   | `Scheduler.prioritize_tasks()` | Sorts tasks by priority (high → medium → low) |
| Chronological sorting | `Scheduler.sort_by_time()` | Sorts tasks by their `scheduled_time` ("HH:MM") |
| Filter by status | `Scheduler.filter_by_status()` | Returns only tasks matching a given `completed` value |
| Filter by pet | `Scheduler.filter_by_pet()` | Returns only the tasks belonging to a named pet. |
| Conflict detection | `Scheduler.detect_conflicts()` | Groups all scheduled tasks by exact `scheduled_time` |
| Recurring tasks | `Task.next_occurrence()`, `Task.mark_complete()`, `Pet.complete_task()` | Tasks carry an optional `recurrence` ("daily"/"weekly") and `due_date`. Completing a recurring task automatically generates the next occurrence, due one interval later (via `timedelta`) |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
