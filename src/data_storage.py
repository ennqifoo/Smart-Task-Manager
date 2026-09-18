import json
from datetime import date
from typing import List
from src.main_task import Task
from src.sub_task import SubTask

def save_to_json(tasks: List[Task], file_path: str) -> bool:
    """
    Save all current tasks into a compact JSON file.
    Optimized for performance (used in H1 performance testing).
    """
    try:
        # Convert tasks and subtasks to plain dicts for JSON serialization
        task_dicts = [
            {
                "task_id": t.task_id,
                "name": t.name,
                "category": t.category,
                "priority": t.priority,
                "deadline": t.deadline.isoformat(),
                "status": t.status,
                "recurrence": t.recurrence,
                "parent_id": t.parent_id,
                "subtask": [
                    {
                        "subtask_id": s.subtask_id,
                        "name": s.name,
                        "priority": s.priority,
                        "deadline": s.deadline.isoformat(),
                        "status": s.status,
                        "prerequisite_id": s.prerequisite_id,
                    }
                    for s in t.subtask
                ],
            }
            for t in tasks
        ]

        # Serialize once in memory (faster than incremental dump)
        json_str = json.dumps(task_dicts, separators=(",", ":"), ensure_ascii=False)

        # Write to disk in a single buffered operation (16 KB buffer)
        with open(file_path, "w", encoding="utf-8", buffering=16384) as f:
            f.write(json_str)

        return True

    except Exception as e:
        print(f"[!] Failed to save tasks: {e}")
        return False


def load_from_json(file_path: str) -> List[Task]:
    """
    Load tasks from a JSON file and reconstruct Task/SubTask objects.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        tasks = []
        for item in data:
            task = Task(
                task_id=item["task_id"],
                name=item["name"],
                category=item["category"],
                priority=item["priority"],
                deadline=date.fromisoformat(item["deadline"]),
                status=item.get("status", "Pending"),
                recurrence=item.get("recurrence"),
                parent_id=item.get("parent_id"),
            )

            # Restore subtasks if available
            for s in item.get("subtask", []):
                subtask = SubTask(
                    subtask_id=s["subtask_id"],
                    name=s["name"],
                    priority=s["priority"],
                    deadline=date.fromisoformat(s["deadline"]),
                    status=s.get("status", "Pending"),
                    prerequisite_id=s.get("prerequisite_id"),
                )
                task.subtask.append(subtask)

            tasks.append(task)

        return tasks

    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"[!] Failed to load tasks: {e}")
        return []
