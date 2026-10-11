import sys
import datetime
import storage

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
        self.commands = ["add", "delete", "edit", "checkbox", "-a", "show"]

    def add(self, command):
        if command == "add":
            if len(self.argv) < 3:
                title = input("Task: ")

            else:
                title = " ".join(self.argv[2:])
                
            description = input("Description: ")

            return title, description
        
        title = self.argv[2]
        description = self.argv[3]

        return title, description

    def delete(self, task_id): 
        ...
    
    def edit(self, command): 
        if len(self.argv) < 3:
            ...

    
    def checkbox(self, task_id): 
        ...

    def show(self):
        task_list = storage.load()
        for task_index in range(len(task_list)):

            print(f'{task_index+1}-', end="")
            print(task_list[task_index]["title"], end="\t\t")
            print(task_list[task_index]["description"])
            print()
        
    
    def run(self):
        task = Default()
        
        task_dict = {
            "title"      :None,
            "description":None,
            "adding date":None,
        }

        if len(self.argv) < 2:
            print("Usage: task <command>")

            return
        
        elif not(self.argv[1] in self.commands):
            print(self.argv[1].rstrip() + " command not found!!")

            return
        
        command = self.argv[1]
        if command in ["add", "-a"]:
            task.title, task.description = self.add(command)

            task_dict["title"] = task.title
            task_dict["description"] = task.description
            task_dict["adding date"] = task.adding_date

            storage.save(task_dict)

        elif command == "show":
            self.show()

        elif command == "edit":
            self.show()
            self.edit()
            


def main():
    TooDoo(sys.argv).run()