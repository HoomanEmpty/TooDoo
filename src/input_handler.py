def input_handler(question = "Value", Type = "str", low_high = (-9.9e100, 9.9e100, "[]"), options = [], default = "", auto_prevention = "", rsls = "", rewrite=(), autofill = True, option_error_massage = f"\nThe answer was not exepted! - Expected answer(s): "):
    data_type = {
        "str" : str,
        "float" : float,
        "int" : int,
        "bool" : bool}

    while True:
        try:
            answer = input(question)
            if answer:

                if Type == "int" or Type == "float":
                    if autofill:
                        if len(options) == 1:
                            options = [number for number in range(options[0] + 1)]
            
                        elif len(options) == 2:
                            options = [number for number in range(options[0], options[1] + 1)]

                else:
                    if autofill:
                        if len(options) == 1:
                            if type(options[0]) == list:
                                options = [title for title in options[0]]

                            else:
                                options = [str(number) for number in range(options[0] + 1)]

                        elif len(options) == 2:
                            if type(options[0]) == list or type(options[1]) == list:

                                if type(options[0]) == list:
                                    backup_options = [str(number) for number in range(options[1] + 1)]
                                    options = backup_options + [title for title in options[0]]

                                else:
                                    backup_options = [str(number) for number in range(options[0] + 1)]
                                    options = backup_options + [title for title in options[1]]

                            else:
                                options = [str(number) for number in range(options[0], options[1] + 1)] 

                        elif len(options) == 3:
                            backup_options = [str(number) for number in range(options[0], options[1] + 1)]
                            options = backup_options + [title for title in options[2]]

                match Type:
                    case "str":
                        match auto_prevention:
                            case "lower":
                                answer = answer.lower()

                            case "upper":
                                answer = answer.upper()

                            case "title":
                                answer = answer.title()

                        match rsls:
                            case "rs":
                                answer = answer.rstrip()

                            case "ls":
                                answer = answer.lstrip()

                            case "rsls":
                                answer = answer.rstrip().lstrip()

                        if rewrite:
                            answer = answer.replace(rewrite[0], rewrite[1])

                        
                        if answer in options or not options:
                            return answer

                        else:
                            print(option_error_massage, [option for option in options])

                    case "int" | "float":
                        answer = data_type[Type](answer)

                        if low_high[2] == "[]":
                            if low_high[0] <= answer <= low_high[1]:
                                if answer in options or not options:
                                    return answer
                                
                                else:
                                    print(option_error_massage, [option for option in options])

                            else:
                                print(f"\nOut of range! Please enter a value between [{low_high[0]}, {low_high[1]}]\n")

                        elif low_high[2] == "()":
                            if low_high[0] < answer < low_high[1]:
                                if answer in options or not options:
                                    return answer

                                else:
                                    print(option_error_massage, [option for option in options])

                            else:
                                print(f"\nOut of range! Please enter a value between ({low_high[0]}, {low_high[1]})\n")

                        
                    case "float":
                        ...

                    case "bool":
                        ...
            
            else:
                return default
        
        except ValueError:
            print(" Invalid input ...")
