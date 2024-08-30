import json, os, sys

TASKS_FILE ="tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def create_task(title):
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "completed": False,
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"The task {title} has been created")

def list_tasks(show_all=True, show_completed=False):
    tasks = load_tasks()
    if not tasks:
        print("The task list is empty")
        return

    filtered_tasks = [t for t in tasks if show_all or t["completed"] == show_completed]
    
    for task in filtered_tasks:
        status = "✓" if task["completed"] else "✗"
        print(f"[{task['id']}] {task['title']} - {status}")

def edit_task(task_id, new_title):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = new_title
            save_tasks(tasks)
            print(f"The task {task_id} has been changed to '{new_title}'.")
            return
    print(f"Task with id {task_id} not found.")

def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [task for task in tasks if task["id"] != task_id]
    if len(tasks) == len(new_tasks):
        print(f"Task with id {task_id} not found")
    else:
        save_tasks(new_tasks)
        print(f"The task {task_id} has been deleted.")

def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            print(f"Task {task_id} marked as completed.")
            return
    print(f"The task {task_id} has been deleted.")

def print_help():
    help_text = """
    Commands:
    -h, --help             - Shows this message
    create <title>         - Creates new task
    list                   - Shows list of your tasks
    complete <id>          - Marks your task as completed
    list-completed         - Shows only completed tasks
    list-pending           - Shows only pending tasks
    edit <id> <new_title>  - Edits the task
    delete <id>            - Deletes the task
    """
    print(help_text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("python task_tracker.py <command> [args]")
        sys.exit(1)

    command = sys.argv[1]

    if command in ("-h", "--help"):
        print_help()

    if command == "create":
        if len(sys.argv) != 3:
            print(f"python task_tracker.py create <title>")
        else:
            create_task(sys.argv[2])
    elif command == "list":
        list_tasks(show_all=True)
    elif command == "list-completed":
        list_tasks(show_all=False, show_completed=True)
    elif command == "list-pending":
        list_tasks(show_all=False, show_completed=False)
    elif command == "edit":
        if len(sys.argv) != 4:
            print('python task_tracker.py edit <id> "new_title"')
        else:
            edit_task(int(sys.argv[2]), sys.argv[3])
    elif command == "delete":
        if len(sys.argv) != 3:
            print("python task_tracker.py delete <id>")
        else:
            delete_task(int(sys.argv[2]))
    elif command == "complete":
        if len(sys.argv) != 3:
            print("python task_tracker.py complete <id>")
        else:
            complete_task(int(sys.argv[2]))
    else:
        print("Unknown command.")