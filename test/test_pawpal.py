import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pawpal_system import Pet, Task


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
