# Smart Task Manager (STM)

A command-line task manager built in Python. Create tasks and subtasks, set deadlines, priorities and categories, track recurring tasks, mark work complete, and view analytics on your progress — all from a simple interactive menu.

## Features

- **Main tasks & subtasks** — break work down, with subtask deadlines constrained to fall on or before their parent task's deadline.
- **Recurring tasks** — mark a task as daily, weekly, or monthly.
- **Categories & priorities** — organize tasks as Work, Personal, Study, or Health, with High/Medium/Low priority.
- **Notifications** — see upcoming deadlines and overdue tasks at a glance.
- **Analytics** — completion rate, task counts (total/completed/pending/overdue), and a breakdown by category, rendered as formatted tables.
- **Persistence** — tasks are saved to `tasks.json` and reloaded automatically the next time you run the app.

## Requirements

- Python 3.10+
- [rich](https://pypi.org/project/rich/) (used for the analytics tables)

## Setup

```bash
# from the project root
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install rich
```

(If a `requirements.txt` is added later, use `pip install -r requirements.txt` instead.)

## Running the app

From the project root:

```bash
python -m src.stm
```

You'll see the main menu:

```
-------------------------------------
| STM: Smart Task Manager Console   |
-------------------------------------
1. Add Task
2. View Tasks
3. View Notifications
4. Edit Task
5. Delete Task
6. Exit
7. Mark Task as Complete
-------------------------------------
```

Enter a number (1–7) and follow the prompts. Your tasks are saved to `tasks.json` automatically when you choose **6. Exit**.

### Adding a task

1. Choose **1. Add Task**, then pick **m** (Main Task) or **s** (SubTask).
2. For a main task: enter a name, pick a category (Work/Personal/Study/Health), pick a priority (High/Medium/Low), and enter a deadline (`YYYY-MM-DD`, today or later).
3. Choose whether it's recurring (daily/weekly/monthly).
4. For a subtask: pick which existing main task it belongs to, then enter a name and deadline (must not be later than the parent's deadline).

### Viewing tasks

Choose **2. View Tasks** to see all tasks and subtasks in a table, followed by an analytics summary (completion rate, totals, and tasks per category).

### Notifications

Choose **3. View Notifications** to list tasks with upcoming deadlines and any that are overdue.

### Editing a task

Choose **4. Edit Task**, select a Main Task by ID, then pick which field to change (name, category, priority, or deadline). Subtask editing isn't supported yet.

### Deleting a task

Choose **5. Delete Task**, pick Main Task or SubTask, select it by ID, and confirm. Deleting a main task also removes its subtasks.

### Marking a task complete

Choose **7. Mark Task as Complete** and select a Main Task by ID. A task can only be marked complete once all of its subtasks are completed. Subtask completion isn't supported yet.

## Project structure

```
src/
  stm.py             # main driver loop
  ui.py              # menus and input/output formatting
  menu_handlers.py    # logic behind each menu option
  main_task.py         # Task model + add/edit/delete
  sub_task.py           # SubTask model
  task_id_manager.py     # unique task ID generation
  data_storage.py          # save/load tasks.json
  analytics.py               # completion rate, summaries
  notification.py             # upcoming/overdue deadline checks
  user_input.py                 # input validation helpers
tests/                           # unit, edge-case, and performance tests
tasks.json                        # saved task data (created/updated by the app)
```

## Running the tests

```bash
python -m unittest discover tests
```

## Author

Foo Enn Qi — built for FIT2107 Software Quality and Testing.
