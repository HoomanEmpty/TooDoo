"""TooDoo - a to-do list manager for the terminal.

Entry point: ``task <command> [arguments]`` (see ``TooDoo.commands`` for the
list of commands and their aliases).
"""
import sys
from datetime import datetime

import display
import input_handler
import storage

DATE_FORMAT = "%Y-%m-%d %a %H:%M:%S"


class Task:
    """Base task: a title, a description and a done flag."""

    def __init__(self, title=None, description=None):
        self.title = title
        self.description = description
        self.done = False

    def to_dict(self):
        """The task as a plain dict, ready to be saved as JSON."""
        return {
            "title": self.title,
            "description": self.description,
            "task_done": self.done,
            "task_id": None,
        }


class Default(Task):
    """A normal task; it also remembers when it was added."""

    def __init__(self, title=None, description=None, adding_date=None):
        super().__init__(title, description)
        # Evaluated when the task is created (not once at import time).
        self.adding_date = adding_date or datetime.now().strftime(DATE_FORMAT)

    def to_dict(self):
        data = super().to_dict()
        data["adding date"] = self.adding_date
        return data


class TooDoo:
    def __init__(self, argv):
        self.argv = argv

        # command group -> all the words that trigger it
        self.commands = {"add": ["add", "-a"],
                         "remove": ["delete", "del", "-d", "rm", "remove"],
                         "edit": ["edit"],
                         "checkbox": ["check", "done", "uncheck", "undone"],
                         "move": ["move", "mv", "amove", "amv"],
                         "show": ["show"],
                         "backup": ["backup", "bc", "-b", "export"],
                         "import": ["import", "-i"]}

    # ------------------------------------------------------------------
    # Helpers shared by several commands
    # ------------------------------------------------------------------

    @staticmethod
    def _ask(question, tasks):
        """Ask the user for a task number or title. Enter returns "0" (cancel)."""
        return input_handler.input_handler(
            question=question,
            options=[len(tasks), [task["title"] for task in tasks]],
            default="0",
            option_error_message="\n This task doesn't exist!! - Expected tasks: ")

    @staticmethod
    def _resolve(tasks, choice):
        """Turn a title or a 1-based number into a list index.

        Returns None if the user cancelled ("0") or the task doesn't exist.
        """
        if choice == "0":
            return None

        for index, task in enumerate(tasks):
            if task["title"] == choice:
                return index

        try:
            number = int(choice)
        except ValueError:
            number = 0

        if 1 <= number <= len(tasks):
            return number - 1

        print("This task doesn't exist!!")
        return None

    def _pick(self, tasks, action):
        """Find the task a command works on.

        The task comes from the command line (``task del 2`` or
        ``task del Some title``); if it isn't given, the list is shown and
        the user is asked. Returns a list index or None.
        """
        if not tasks:
            print("No task added!!!")
            return None

        if len(self.argv) < 3:
            self.show()
            choice = self._ask(f"Which task do you want to {action}: ", tasks)
        else:
            choice = " ".join(self.argv[2:])

        return self._resolve(tasks, choice)

    # ------------------------------------------------------------------
    # Commands
    # ------------------------------------------------------------------

    def _read_new_task(self, command):
        """Get the title and description of a new task.

        ``task add [title]``       -> missing values are asked for
        ``task -a title desc``     -> both values come from the command line
        """
        argv = self.argv

        if command == "add":
            title = " ".join(argv[2:]) if len(argv) > 2 else input("Task: ")
            description = input("Description: ")
        else:
            title = argv[2] if len(argv) > 2 else input("Task: ")
            description = argv[3] if len(argv) > 3 else input("Description: ")

        return title, description

    @staticmethod
    def _read_edited_task(old_title, old_description):
        """Ask for a new title and description; Enter keeps the old value."""
        title = input(f"{old_title} change to: ") or old_title
        description = input("Enter description: ") or old_description

        return title, description

    def add(self, command):
        title, description = self._read_new_task(command)
        storage.append(Default(title, description).to_dict())

    def delete(self):
        tasks = storage.load()
        index = self._pick(tasks, "delete")
        if index is None:
            return

        del tasks[index]
        storage.save(tasks)

    def edit(self):
        tasks = storage.load()
        index = self._pick(tasks, "edit")
        if index is None:
            return

        task = tasks[index]
        task["title"], task["description"] = self._read_edited_task(
            task["title"], task["description"])
        storage.save(tasks)

    def checkbox(self, command):
        """check / done mark a task as done; uncheck / undone undo it."""
        done = command in ("check", "done")

        tasks = storage.load()
        index = self._pick(tasks, "check" if done else "uncheck")
        if index is None:
            return

        tasks[index]["task_done"] = done
        storage.save(tasks)

    def show(self):
        tasks = storage.load()
        if not tasks:
            print("No task added!!!")
            return

        display.print_tasks(tasks)

    def move(self):
        """move / mv put a task at a new position; amove / amv swap two tasks."""
        tasks = storage.load()
        if not tasks:
            print("No task added!!!")
            return

        # Anything missing from the command line is asked for.
        if len(self.argv) < 4:
            self.show()

        source = (self.argv[2] if len(self.argv) > 2
                  else self._ask("Which task do you want to move: ", tasks))
        target = (self.argv[3] if len(self.argv) > 3
                  else self._ask("Where you want put your task: ", tasks))

        source = self._resolve(tasks, source)
        if source is None:
            return

        target = self._resolve(tasks, target)
        if target is None:
            return

        if self.argv[1] in ("amove", "amv"):
            tasks[source], tasks[target] = tasks[target], tasks[source]
        else:
            tasks.insert(target, tasks.pop(source))

        storage.save(tasks)

    # ------------------------------------------------------------------
    # Dispatching
    # ------------------------------------------------------------------

    def run(self):
        if len(self.argv) < 2:
            print("Usage: task <command>")
            return

        command = self.argv[1]

        # Find which command group the typed word belongs to.
        group = next((name for name, words in self.commands.items()
                      if command in words), None)

        if group is None:
            print(command.rstrip() + " command not found!!")
            return

        handlers = {
            "add": lambda: self.add(command),
            "remove": self.delete,
            "edit": self.edit,
            "checkbox": lambda: self.checkbox(command),
            "move": self.move,
            "show": self.show,
            "backup": lambda: storage.backup(command),
            "import": lambda: storage.imp(command),
        }
        handlers[group]()


def main():
    TooDoo(sys.argv).run()


if __name__ == "__main__":
    main()