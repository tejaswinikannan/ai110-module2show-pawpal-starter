"""Core implementation for PawPal+, generated from diagrams/uml.mmd."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import ClassVar, Optional

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
DEFAULT_TASK_DURATIONS = {"feed": 10, "walk": 30}


@dataclass
class Owner:
    name: str
    number_of_pets: int = 0
    pets: list["Pet"] = field(default_factory=list)

    @classmethod
    def create_owner(cls, name: str) -> "Owner":
        """Create a new Owner with no pets yet."""
        return cls(name=name, number_of_pets=0, pets=[])

    def add_pet(self, pet: "Pet") -> "Pet":
        """Register a pet with this owner and keep the pet count in sync."""
        self.pets.append(pet)
        self.number_of_pets = len(self.pets)
        return pet


@dataclass
class Pet:
    pet_type: str
    name: str
    tasks: list["Task"] = field(default_factory=list)

    @classmethod
    def add_pet(cls, pet_type: str, name: str) -> "Pet":
        """Create a new Pet with no tasks yet."""
        return cls(pet_type=pet_type, name=name, tasks=[])

    def feed(self) -> None:
        """Add a feeding task to this pet's task list."""
        task = Task.add_task("Feeding", duration_minutes=DEFAULT_TASK_DURATIONS["feed"], priority="high")
        self.tasks.append(task)

    def schedule_walk(self) -> None:
        """Add a walk task to this pet's task list."""
        task = Task.add_task("Walk", duration_minutes=DEFAULT_TASK_DURATIONS["walk"], priority="medium")
        self.tasks.append(task)


@dataclass
class Task:
    task_title: str
    task_id: int
    duration_minutes: int = 20
    priority: str = "medium"
    scheduled_time: Optional[str] = None
    completed: bool = False

    _next_id: ClassVar[int] = 1

    @classmethod
    def add_task(cls, task_title: str, duration_minutes: int = 20, priority: str = "medium") -> "Task":
        """Create a new Task with an auto-assigned, unique task_id."""
        task = cls(task_title=task_title, task_id=cls._next_id, duration_minutes=duration_minutes, priority=priority)
        cls._next_id += 1
        return task

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def view_tasks(self) -> list:
        """Return this task's fields as a single-row, display-ready list."""
        return [
            {
                "task_id": self.task_id,
                "task_title": self.task_title,
                "duration_minutes": self.duration_minutes,
                "priority": self.priority,
                "scheduled_time": self.scheduled_time,
                "completed": self.completed,
            }
        ]


@dataclass
class Scheduler:
    task_id: int = 0
    task_title: str = ""
    task_time: str = ""

    def prioritize_tasks(self, tasks: list["Task"]) -> list["Task"]:
        """Sort tasks by priority (high first), then by shorter duration."""
        return sorted(
            tasks,
            key=lambda t: (PRIORITY_ORDER.get(t.priority, len(PRIORITY_ORDER)), t.duration_minutes),
        )

    def sort_by_time(self, tasks: list["Task"]) -> list["Task"]:
        """Sort tasks chronologically by scheduled_time ("HH:MM"), unscheduled tasks last."""
        return sorted(tasks, key=lambda t: (t.scheduled_time is None, t.scheduled_time))

    def view_daily_routines(self, owner: Owner) -> list:
        """Return every task across all of an owner's pets."""
        return [task for pet in owner.pets for task in pet.tasks]

    def filter_by_status(self, tasks: list["Task"], completed: bool) -> list["Task"]:
        """Return only the tasks matching the given completion status."""
        return [task for task in tasks if task.completed == completed]

    def filter_by_pet(self, owner: Owner, pet_name: str) -> list["Task"]:
        """Return the tasks belonging to the pet with the given name."""
        return [task for pet in owner.pets for task in pet.tasks if pet.name == pet_name]

    def build_daily_schedule(
        self, owner: Owner, start_time: str = "08:00", available_minutes: Optional[int] = None
    ) -> list["Task"]:
        """Prioritize an owner's tasks and assign start times, skipping any that don't fit in available_minutes."""
        tasks = self.prioritize_tasks(self.view_daily_routines(owner))
        current_time = datetime.strptime(start_time, "%H:%M")
        elapsed_minutes = 0
        schedule: list[Task] = []

        for task in tasks:
            if task.completed:
                continue
            if available_minutes is not None and elapsed_minutes + task.duration_minutes > available_minutes:
                continue
            task.scheduled_time = current_time.strftime("%H:%M")
            schedule.append(task)
            current_time += timedelta(minutes=task.duration_minutes)
            elapsed_minutes += task.duration_minutes

        return schedule
