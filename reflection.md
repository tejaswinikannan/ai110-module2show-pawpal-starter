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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- `detect_conflicts` only flags tasks with the exact same `scheduled_time` string; it doesn't check for overlapping time ranges (e.g., a 08:00-08:30 task and a 08:15-08:20 task wouldn't be caught).
- This is reasonable because `build_daily_schedule` always assigns times back-to-back, so true overlaps can only come from a manually pinned time (like a vet appointment). A simple grouping check (`O(n)`) covers that case without the added complexity of interval-overlap math (`O(n²)`), at the cost of occasionally missing a partial overlap rather than raising false alarms.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
