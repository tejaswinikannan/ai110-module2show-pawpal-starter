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
        return cls(name=name, number_of_pets=0, pets=[])

    def add_pet(self, pet: "Pet") -> "Pet":
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
        return cls(pet_type=pet_type, name=name, tasks=[])

    def feed(self) -> None:
        task = Task.add_task("Feeding", duration_minutes=DEFAULT_TASK_DURATIONS["feed"], priority="high")
        self.tasks.append(task)

    def schedule_walk(self) -> None:
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
        task = cls(task_title=task_title, task_id=cls._next_id, duration_minutes=duration_minutes, priority=priority)
        cls._next_id += 1
        return task

    def view_tasks(self) -> list:
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
        return sorted(
            tasks,
            key=lambda t: (PRIORITY_ORDER.get(t.priority, len(PRIORITY_ORDER)), t.duration_minutes),
        )

    def view_daily_routines(self, owner: Owner) -> list:
        return [task for pet in owner.pets for task in pet.tasks]

    def build_daily_schedule(
        self, owner: Owner, start_time: str = "08:00", available_minutes: Optional[int] = None
    ) -> list["Task"]:
        """Order an owner's pending tasks by priority and assign start times.

        Stops adding tasks once `available_minutes` would be exceeded, so a
        busy owner still gets a schedule that fits in the time they actually have.
        """
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
