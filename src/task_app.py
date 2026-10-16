import sys
import datetime
import storage
import input_handler

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
        self.commands = ["add", "delete", "edit", "checkbox", "-a", "show", "del", "-d", "mv", "move"]

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


    def delete(self):
        tasks = storage.load()
        titles = storage.load("title")

        if len(self.argv) < 3:
            self.show()
            user_choice = input_handler.input_handler(question="Which task do you want to delete: ", Type="str", options=[storage.load("len"), storage.load("title")], auto_prevention="", default=0, option_error_massage="\n This task doesn't exist!! - Expected tasks: ")
            
            try:
                user_choice = int(user_choice)
                if user_choice == 0:
                    return
                
                del tasks[user_choice - 1]
                storage.save(tasks)
                return
                
            except:
                for task_index in range(len(tasks)):
                    if user_choice == tasks[task_index]["title"]:
                        del tasks[task_index]
                        storage.save(tasks)
                        return

        else:
            task_title = " ".join(self.argv[2:])

            if task_title == "0":
                return
            
            for task_index in range(len(tasks)):
                if task_title == tasks[task_index]["title"]:
                    del tasks[task_index]
                    storage.save(tasks)
                    return

            try:        
                del tasks[int(self.argv[2]) - 1]
                storage.save(tasks)
                return

            except:
                print("This task doesn't exist!!")
                return

        

    
    def edit(self, command): 
        if len(self.argv) < 3:
            self.show()
            user_choice = input_handler.input_handler(question="Wich task you want edit: ", Type=int, options=[storage.load("len")], default=0)

    
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

        elif command in ["delete", "del", "-d"]:
            self.delete()


def main():
    TooDoo(sys.argv).run()