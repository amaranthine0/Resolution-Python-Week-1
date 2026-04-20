import argparse
import sys
import os
import json

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save_task(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

parser = argparse.ArgumentParser()
parser.add_argument("task", type=str, nargs="?", help="Task to add")
parser.add_argument("-c", "--complete", type=int, help="Mark a task as complete by ID")
parser.add_argument("-d", "--delete", type=int, help="Delete a task by ID")
parser.add_argument("-l", "--list", help="List all tasks", action="store_true")
parser.add_argument("-D", "--difficulty", type=int, choices=[1,2,3], help="set the difficulty level of the task")
parser.add_argument("-r", "--reverse", action="store_true", help="reverses the order of tasks")
args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

if args.list:
    tasks = load_tasks()
    for task in tasks:
        status = "x" if task["done"] else " "
        difficulty = task.get("difficulty", "N/A")
        print(f"[{status}] {task['id']}: {task['task']} (difficulty: {difficulty})")
    sys.exit(0)
elif args.complete:
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == args.complete:
            task["done"] = True
            save_task(tasks)
            print(f"Task {args.complete} marked as complete")
            break
elif args.delete:
    tasks = load_tasks()
    new_tasks = []
    for task in tasks:
        if task["id"] != args.delete:
            new_tasks.append(task)
    save_task(new_tasks)
    print(f"Task with ID of {args.delete} deleted")
elif args.task:
    tasks = load_tasks()
    new_id = tasks[-1]["id"] + 1 if tasks else 1
    tasks.append({"id": new_id, "task": args.task, "done": False, "difficulty": args.difficulty})
    save_task(tasks)
    print(f"Task '{args.task}' added with ID {new_id} (difficulty: {args.difficulty})")
elif args.reverse:
    tasks = load_tasks()
    total = len(tasks) - 1
    new_tasks = [0] * (total + 1)
    for task in tasks:
        new_tasks[total] = task
        total-=1
    save_task(new_tasks)
    print(f"Order of array has been reversed")