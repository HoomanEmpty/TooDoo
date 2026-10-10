import sys
import datetime
class Task:
    def __init__(self, title=None, description=None):
        self.title = title
        self.description = description
        self.done = False

class Default(Task):
    def __init__(self, title=None, description=None, adding_date=datetime.datetime.now().strftime("%Y-%m-%d %a %H:%M:%S")):
        super().__init__(title, description)
        self.adding_date = adding_date

class TooDoo:
    def __init__(self, argv):
        self.argv = argv
        self.tasks = []
        self.commands = ["add", "delete", "edit", "checkbox", "-a"]

    def add(self, topic):
        if topic == "add": 
            if len(self.argv) < 3:
                title = input("Task: ")

                return title

            title = " ".join(self.argv[2:])
            
            return title
        
        elif topic == "description":
            description = input("Description: ")

            return description


    def delete(self, task_id): 
        ...
    
    def edit(self, task_id): 
        ...
    
    def checkbox(self, task_id): 
        ...

    def run(self):
        task = Default()

        if len(self.argv) < 2:
            print("Usage: task <command>")

            return
        
        elif not(self.argv[1] in self.commands):
            print(self.argv[1].rstrip() + " command not found!!")

            return
        
        command = self.argv[1]
        if command == "add":
            task.title       = self.add("add")
            task.description = self.add("description")


def main():
    TooDoo(sys.argv).run()