# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

```
Classes: Owner, Pet, Task, Scheduler
Owner class:
    Attributes: name, no of pets
    Methods: Create owner
Pet class:
    Attributes: pet type,
    Methods: Add a pet, Feed the pet, schedule a walk
Task class:
    Attributes: task title, task id
    Methods: View tasks, Add tasks
Scheduler class:
    Attributes: task id, task title, task time
    Methods: Prioritize tasks, View Daily routines
```

**b. Design changes**

- Added the view daily routines method to the scheduler class
- Added a `pets` list attribute to `Owner` and a `tasks` list attribute to `Pet`, so the Scheduler can traverse `Owner -> Pet -> Task` to collect all tasks across an owner's pets
- Updated `Scheduler.viewDailyRoutines()` to take an `Owner` as a parameter and return the flattened list of tasks from all of that owner's pets
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

  My scheduler considers four constraints, in this order of precedence:
  1. **Priority** — `prioritize_tasks()` sorts by `PRIORITY_ORDER` (`high` → `medium` → `low`) first, so urgent care (feeding, meds) is always placed ahead of lower-stakes tasks (grooming) regardless of when they were added.
  2. **Duration** — used as the tiebreaker within the same priority tier (shorter tasks first), so a tight schedule fits more same-priority tasks rather than getting blocked by one long one.
  3. **Available time** — `build_daily_schedule()` takes a `start_time` and an optional `available_minutes` budget; it walks the prioritized list and skips (rather than truncates or reorders) any task that would push the running total past the budget.
  4. **Completion status** — already-`completed` tasks are skipped when building a new schedule, so finished work doesn't reappear or eat into the time budget.

  I did not implement an explicit "owner preferences" constraint (e.g., preferred walk times) — everything is either priority-driven or duration-driven right now.

- How did you decide which constraints mattered most?

  I ranked priority above duration because in a pet-care context, missing a high-priority task (feeding, medication) has real consequences, while a low-priority task (grooming) slipping to tomorrow doesn't. Duration only matters as a secondary signal — it's a simple greedy heuristic to pack more tasks into a limited window, not a true optimizer, but it's proportional to the actual complexity this project needed.

**b. Tradeoffs**

- `detect_conflicts` only flags tasks with the exact same `scheduled_time` string; it doesn't check for overlapping time ranges (e.g., a 08:00-08:30 task and a 08:15-08:20 task wouldn't be caught).
- This is reasonable because `build_daily_schedule` always assigns times back-to-back, so true overlaps can only come from a manually pinned time (like a vet appointment). A simple grouping check (`O(n)`) covers that case without the added complexity of interval-overlap math (`O(n²)`), at the cost of occasionally missing a partial overlap rather than raising false alarms.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI mainly for design brainstorming — working through which classes, attributes, and relationships made sense before committing them to the UML diagram. During implementation, whenever the AI generated Pythonic code that was too dense or clever to read comfortably, I'd flag the specific lines, ask it to explain its reasoning, and then either simplify it myself or have it refactor toward something more readable.
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
AI suggestions were correct most of the time, but I still applied my own judgment to verify each one rather than accepting it at face value.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

  Mainly three things: sorting (does `sort_by_time` actually put tasks in chronological order, and what happens with unscheduled or empty tasks), recurrence (does completing a daily/weekly task correctly spawn the next one a day/week later), and conflict detection (does it catch two tasks at the same time, and stay quiet when it shouldn't flag anything).

- Why were these tests important?

  These are the three behaviors most likely to silently give a pet owner wrong information — a bad sort order, a recurring task that never comes back, or a missed double-booking. They're also the easiest to get subtly wrong (off-by-one on the date math, `None` handling in sorting), so I wanted them locked down.

**b. Confidence**

- How confident are you that your scheduler works correctly?

  Pretty confident for the cases I tested — all 15 tests pass and they cover the core logic plus the obvious edge cases. I'd put it around 4/5; the one thing holding me back is that conflict detection only catches exact time matches, not overlapping ranges, so I know there's a gap.

- What edge cases would you test next if you had more time?

  Overlapping (not identical) time ranges, a task whose duration exactly maxes out `available_minutes`, completing several recurring tasks in a row to make sure IDs and dates don't collide, and what happens if two pets have the same name.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I'm most satisfied with the systematic, iterative approach I took: starting from a bare skeleton and building out implementation logic one piece at a time, while consistently enforcing object-oriented, modular design. I also held myself to coding standards throughout — using decorators and docstrings appropriately, keeping documentation updated as the design evolved, and committing incrementally after each feature rather than in one large batch.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

  I'd rework `detect_conflicts` to check for overlapping time ranges instead of exact time matches, and add a real "owner preferences" constraint (like preferred task windows) instead of scheduling purely by priority and duration.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
One important lesson was that system design and implementation are not a strictly linear process, but an iterative one: I built implementation logic from the initial design, then revisited and reworked that design as the implementation surfaced new requirements. Each implementation change was paired with corresponding updates to the pytest suite to keep the tests aligned with the current behavior. AI assistance made this back-and-forth between design, implementation, and testing considerably smoother to manage.
