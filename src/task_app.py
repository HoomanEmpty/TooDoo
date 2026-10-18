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
        self.commands = {"add":["add", "-a"],
                         "remove":["delete", "del", "-d", "rm", "remove"],
                         "edit":["edit"],
                         "checkbox":["check", "done", "uncheck", "undone"],
                         "move":["move", "mv"],
                         "show":["show"]}

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

    
    def checkbox(self, command): 
        tasks = storage.load()
        if command in ["check", "done"]:
            if len(self.argv) < 3:
                self.show()
                user_choice = input_handler.input_handler(question="Which task do you want to cheked: ", Type="str", options=[storage.load("len"), storage.load("title")], auto_prevention="", default=0, option_error_massage="\n This task doesn't exist!! - Expected tasks: ")
                
                try:
                    user_choice = int(user_choice)
                    if user_choice == 0:
                        return
                    
                    tasks[user_choice - 1]["task_done"] = True
                    storage.save(tasks)
                    return
                    
                except:
                    for task_index in range(len(tasks)):
                        if user_choice == tasks[task_index]["title"]:
                            tasks[task_index]["task_done"] = True
                            storage.save(tasks)
                            return

            else:
                task_title = " ".join(self.argv[2:])

                if task_title == "0":
                    return
                
                for task_index in range(len(tasks)):
                    if task_title == tasks[task_index]["title"]:
                        tasks[task_index]["task_done"] = True
                        storage.save(tasks)
                        return

                try:        
                    tasks[int(self.argv[2]) - 1]["task_done"] = True
                    storage.save(tasks)
                    return

                except:
                    print("This task doesn't exist!!")
                    return

        else:
            if len(self.argv) < 3:
                self.show()
                user_choice = input_handler.input_handler(question="Which task do you want to uncheked: ", Type="str", options=[storage.load("len"), storage.load("title")], auto_prevention="", default=0, option_error_massage="\n This task doesn't exist!! - Expected tasks: ")
                
                try:
                    user_choice = int(user_choice)
                    if user_choice == 0:
                        return
                    
                    tasks[user_choice - 1]["task_done"] = False
                    storage.save(tasks)
                    return
                    
                except:
                    for task_index in range(len(tasks)):
                        if user_choice == tasks[task_index]["title"]:
                            tasks[task_index]["task_done"] = False
                            storage.save(tasks)
                            return

            else:
                task_title = " ".join(self.argv[2:])

                if task_title == "0":
                    return
                
                for task_index in range(len(tasks)):
                    if task_title == tasks[task_index]["title"]:
                        tasks[task_index]["task_done"] = False
                        storage.save(tasks)
                        return

                try:        
                    tasks[int(self.argv[2]) - 1]["task_done"] = False
                    storage.save(tasks)
                    return

                except:
                    print("This task doesn't exist!!")
                    return  

    def show(self):
        task_list = storage.load()
        for task_index in range(len(task_list)):

            print(f'{task_index+1}-', end="")
            print(task_list[task_index]["title"], end="")
            if task_list[task_index]["task_done"] == True:
                print(" ✅", end="\t\t")
            
            else:
                print("", end="\t\t")

            print(task_list[task_index]["description"])
            print()
        
    
    def run(self):
        task = Default()
        
        task_dict = {
            "title"      :None,
            "description":None,
            "adding date":None,
            "task_done":False,
            "task_id":None,
        }

        if len(self.argv) < 2:
            print("Usage: task <command>")
            return
        
        else:
            for cmd in self.commands:
                if self.argv[1] in cmd:
                    command = self.argv[1]
                    break

            print(self.argv[1].rstrip() + " command not found!!")

        if command in self.commands["add"]:
            task.title, task.description = self.add(command)

            task_dict["title"] = task.title
            task_dict["description"] = task.description
            task_dict["adding date"] = task.adding_date

            storage.save(task_dict)

        elif command in self.commands["show"]:
            self.show()

        elif command in self.commands["edit"]:
            self.edit()

        elif command in self.commands["remove"]:
            self.delete()

        elif command in self.commands["checkbox"]:
            self.checkbox(command)


def main():
    TooDoo(sys.argv).run()