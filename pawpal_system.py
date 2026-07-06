"""Class skeletons for PawPal+, generated from diagrams/uml.mmd."""

from dataclasses import dataclass


@dataclass
class Owner:
    name: str
    number_of_pets: int
    pets: list["Pet"]

    def create_owner(self) -> "Owner":
        pass


@dataclass
class Pet:
    pet_type: str
    name: str
    tasks: list["Task"]

    def add_pet(self) -> "Pet":
        pass

    def feed(self) -> None:
        pass

    def schedule_walk(self) -> None:
        pass


@dataclass
class Task:
    task_title: str
    task_id: int

    def view_tasks(self) -> list:
        pass

    def add_task(self) -> None:
        pass


@dataclass
class Scheduler:
    task_id: int
    task_title: str
    task_time: str

    def prioritize_tasks(self) -> list:
        pass

    def view_daily_routines(self, owner: Owner) -> list:
        return [task for pet in owner.pets for task in pet.tasks]
