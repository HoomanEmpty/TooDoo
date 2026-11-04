"""Storage layer: keeps the tasks in a JSON file and handles backup / import."""
import json
import shutil
from pathlib import Path

DATA_DIR = Path.home() / ".config" / "TooDoo"
TASKS_FILE = DATA_DIR / "tasks.txt"
BACKUP_NAME = "TooDoo.backup.Jaraare"


# ---------------------------------------------------------------------------
# Reading and writing tasks
# ---------------------------------------------------------------------------

def load():
    """Return the list of saved tasks (an empty list if nothing is saved yet)."""
    if not TASKS_FILE.exists():
        return []

    return json.loads(TASKS_FILE.read_text(encoding="utf-8"))


def save(tasks):
    """Overwrite the task file with the given list of tasks."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TASKS_FILE.write_text(json.dumps(tasks), encoding="utf-8")


def append(task):
    """Add one task (a dict) to the end of the saved tasks."""
    tasks = load()
    tasks.append(task)
    save(tasks)


# ---------------------------------------------------------------------------
# Backup and import
# ---------------------------------------------------------------------------

def _ask_directory(question):
    """Ask for a directory. Enter = home folder, "0" = cancel (returns None)."""
    answer = input(question).strip()

    if answer == "0":
        return None

    if not answer:
        return Path.home()

    return Path(answer).expanduser()  # also understands "~" and "~/folder"


def backup(command):
    """Copy the task file to a backup file.

    "-b" saves straight into the home folder; otherwise the user is asked
    where to save it.
    """
    if not TASKS_FILE.exists():
        print("No task added!!!")
        return

    if command == "-b":
        folder = Path.home()

    else:
        while True:
            folder = _ask_directory("Where you want save your backup: ")
            if folder is None:
                return

            if folder.is_dir():
                break

            print("Path doesn't exist!!!")

    shutil.copy2(TASKS_FILE, folder / BACKUP_NAME)
    print(f"Backup is saved in {folder / BACKUP_NAME}")


def imp(command):
    """Restore the tasks from a backup file (the backup file is moved, not copied).

    "-i" looks for the backup in the home folder; otherwise the user is asked
    where it is.
    """
    if command == "-i":
        source = Path.home() / BACKUP_NAME
        if not source.exists():
            print("File doesn't exist!!!")
            return

    else:
        while True:
            folder = _ask_directory("Where your backup are saved: ")
            if folder is None:
                return

            source = folder / BACKUP_NAME
            if source.exists():
                break

            print("File doesn't exist!!!")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    shutil.move(source, TASKS_FILE)
    print("Import succeeded!!")