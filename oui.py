"""
OUI, The esolang that talks with you in a wierd way(s).

Written By Zoda:
    Links:
        - https://zoda-service.web.tr/code
        - https://github.com/kerem3338

Licensed under MIT license.

You can learn more about OUI in README.md file.
"""
import json
import argparse
import random
import sys
import time
import os

__version__ = "0.2.0"

rnd_messages = [
    "Do you know you have rights?",
    "Try The D Programming Language.",
    "Who even reads that?",
    "*- 404 -*",
    "I hate everyone",
    "Good luck!",
    f"My lucky number is {random.randint(0,10)}",
    f"{'I hate you' if random.randint(0,1) == 1 else 'I don\' hate you'}",
    "Made in Turkey!",
]

holly_words = [
    "if", "i can", "make", "the",
    "world", "holly", "you", "can", "say",
    "what", "who is", "responsible", "to", "god", "good", "compiler", "witch", "tool",
]

class Errors:
    var_not_founded = "variable not found! variable '{var}' not founded"
    unknown_operation = "unknown operation! '{operation}' is not recognized as a operation by OUI Commitie"
    argument_error = "argument error! '{location}' needs exactly {required} arguments, not {got}"
    var_value_error = "value error! '{e}' at '{location}' (variable name = '{var_name}')"
    value_error = "value error! '{e}' at '{location}'"

def colored(r, g, b, text) -> str:
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def get_number(src) -> float:
    return float(src)

def get_bool(src) -> bool:
    """Get bool from src"""
    if src in ["true","TT"]:
        return True
    elif src in ["false","FF"]:
        return False
    else: raise Exception("Invalid bool")

def get_string(src, report=False):
    """Get string from src"""
    _ = ""
    str_open = -1
    str_end  = -1
    for i, v in enumerate(src):
        if v == "'":
            if str_open == -1:
                str_open = i
                continue
            else:
                str_end = i
                break

        if str_open != -1 and str_end == -1:
            _ += v

    valid = (str_open != -1 and str_end != -1)
    return (_, valid) if report else _


def get_from_type(inp, type):
    """Get value from input and type"""
    if type == "bool":
        return get_bool(inp)
    elif type == "string":
        string_check = get_string(inp)
        if string_check == "":
            raise Exception("*invalid syntax*")
        else: return string_check
    elif type == "number":
        return get_number(inp)
    else: raise Exception("Unknown type")

def get_type_from_str(src) -> str:
    """Get type of src"""
    if len(src) >= 1:
        if src[0].isnumeric():
            return "number"
        else:
            if src in ["true","false","TT","FF"]:
                return "bool"
            else:
                return "string"
    raise Exception("source 'src' len must be at least 1")

def exact_arg_require(required, errors, got, location) -> bool:
    """Exact argument error handler"""
    if got != required:
        errors.append(Errors.argument_error.format(location = location, required = required, got = got))
        return False

    return True

def get_number_from_list_or_error(work_list, errors, location, convert_int = False) -> list[list,bool]:
    """Function name is the description..."""
    _ = []
    is_ok = True
    for list_val in work_list:
        try:
            number = get_number(list_val)
        except Exception as e:
            errors.append(Errors.value_error.format(e=e, location=location))
            is_ok = False
        else:
            if convert_int:
                number = int(number)

            _.append(number)

    return (_, is_ok)

def get_string_or_error(src, errors, location) -> str or bool:
    """Get string from src or append error"""
    _str = get_string(src, True)
    if _str[1] is False:
        errors.append(Errors.value_error.format(e='not a valid string!', location=location))
        return False
    else:
        return _str[0]

def execute(src, welcome_text = True):
    """Magic function."""
    if welcome_text:
        print(colored(0,127,127,f'OUI Interpreter ({__version__})\n\nRandom message for you:\n\t{random.choice(rnd_messages)}\n'))

    variables = {
        "propaganda": "I'm the selected programming language.",
        "error count": 0
    }

    system_variables = {
        "error variable not exists flag": False
    }

    errors = []
    current = 0

    operations = []
    for op in src.split("---"):
        op = op.strip()
        if op == "": continue
        parts = [part for part in op.split("|") if part.strip() != ""]

        operations.append(parts)

    # More magic.
    for op_i, op in enumerate(operations):
        op_name = op[0]
        match op_name:
            case 'set-var':
                if not exact_arg_require(3, errors, len(op), op_name): continue
                
                var_name = get_string_or_error(op[1], errors, op_name)
                if var_name is False: continue

                try:
                    variables[var_name] = get_from_type(op[2],get_type_from_str(op[2]))
                except Exception as e:
                    errors.append(Errors.var_value_error.format(e=e, location=op_name, var_name = var_name))
            
            case 'do nothing for <x> amount of time':
                if not exact_arg_require(2, errors, len(op), op_name): continue

                try:
                    wait_time = get_number(op[1])
                except Exception as e:
                    errors.append(Errors.value_error.format(e=e, location=op_name))
                    continue

                time.sleep(wait_time)

            case 'get input':
                if not exact_arg_require(2, errors, len(op), op_name): continue
                
                var_name = get_string_or_error(op[1], errors, op_name)
                if var_name is False: continue

                variables[var_name] = input("?> ")

            case 'number++':
                if not exact_arg_require(2, errors, len(op), op_name): continue
            
                var_name = get_string_or_error(op[1], errors, op_name)
                if var_name is False: continue

                if not var_name in variables:
                    errors.append(Errors.var_not_founded.format(var=var_name))
                    continue

                if not isinstance(variables[var_name], float):
                    errors.append(Errors.var_value_error.format(e="variable is not a number", location=op_name, var_name=variables[var_name]))
                    continue

                variables[var_name] += 1

            case 'number--':
                if not exact_arg_require(2, errors, len(op), op_name): continue
            
                var_name = get_string_or_error(op[1], errors, op_name)
                if var_name is False: continue

                if not var_name in variables:
                    errors.append(Errors.var_not_founded.format(var=var_name))
                    continue

                if not isinstance(variables[var_name], float):
                    errors.append(Errors.var_value_error.format(e="variable is not a number", location=op_name, var_name=variables[var_name]))
                    continue

                variables[var_name] -= 1

            case 'del-var':
                if not exact_arg_require(2, errors, len(op), op_name): continue
                
                var_name = get_string_or_error(op[1], errors, op_name)
                if var_name is False: continue

                if not var_name in variables:
                    errors.append(Errors.var_not_founded.format(var=var_name))
                    continue

                variables.pop(var_name)
            
            case 'rgb print':
                if not exact_arg_require(5, errors, len(op), op_name): continue

                rgb_values = get_number_from_list_or_error(op[1:4], errors, op_name, convert_int = True)
                if rgb_values[1] is False: continue

                print(colored(*rgb_values[0],get_from_type(op[4],get_type_from_str(op[4]))))

            case 'print':
                for arg in op[1:]:
                    print(get_from_type(arg,get_type_from_str(arg)))

            case 'add 4 spaces to output':
                print("    ", end="")

            case 'print but use spaces instead of newline' | 'print with space':
                for arg in op[1:]:
                    print(get_from_type(arg,get_type_from_str(arg)), end=" ")

            case 'print <x> == <y>':
                if not exact_arg_require(3, errors, len(op), op_name): continue
                val1_raw = op[1]
                val2_raw = op[2]

                try:
                    type1 = get_type_from_str(val1_raw)
                    type2 = get_type_from_str(val2_raw)
                    val1 = get_from_type(val1_raw, type1)
                    val2 = get_from_type(val2_raw, type2)

                    if val1 == val2:
                        print(f"{val1} == {val2}")
                    else: print(f"{val1} != {val2}")
                except Exception as e:
                    errors.append(Errors.value_error.format(e=e, location=op_name))
                    continue

            case 'speak to me':
                generated = ' '.join([random.choice(holly_words) for i in range(random.randint(2,20))])
                print(generated)

            case '...': ...

            case 'normal exit':
                break

            case 'force exit':
                sys.exit(random.randint(0,99))

            case 'force exit if you want':
                if random.randint(0,100) >= 50:
                    sys.exit(1)
                else:
                    print("<execution continues>")

            case 'normal exit if you want':
                if random.randint(0,100) >= 50:
                    sys.exit(1)
                else:
                    print("<execution continues>")

            case '##': ...

            case 'real location':
                print(op_i)
                
            case 'print_var_if_exists' | 'print var if exists':
                for arg in op[1:]:
                    var_name = get_string_or_error(arg, errors, op_name)
                    if var_name is False: continue

                    if var_name in variables:
                        print(variables[var_name])
            
            case 'newline':
                print()

            case 'print all variables':
                print(json.dumps(variables, indent = 4))

            case 'print_var' | 'print var':
                for arg in op[1:]:
                    var_name = get_string_or_error(arg, errors, op_name)
                    if var_name is False: continue

                    if not var_name in variables:
                        errors.append(Errors.var_not_founded.format(var=var_name))
                        continue
                    print(variables[var_name])
            case _:
                errors.append(Errors.unknown_operation.format(operation=op_name))
                if not "error count" in variables:
                    if system_variables["error variable not exists flag"] == False:
                        print(colored(255,0,0,"I'm trying to increment 'error count' variable, but i couldn't find it. Do you know anything about this?"))
                        system_variables["error variable not exists flag"] = True
                else: variables["error count"] += 1

    print(f"\nExecution completed with ({len(errors)}) errors")
    if len(errors) == 0:
        print("-> Good Work!")
        
    for i, error in enumerate(errors):
        # You can't say 'FIX THE ERROR 0!' to someone... or if you can?
        print(f"\t├ {i + 1}) ", error)

if __name__ == "__main__":
    # A little hack for ANSI escape codes
    os.system("")

    if len(sys.argv) == 1:
        sys.argv.append("--repl")

    arg_parser = argparse.ArgumentParser(description="OUI Interpreter")
    arg_parser.add_argument("file", help="File to run", nargs="?", type=argparse.FileType('r'))
    arg_parser.add_argument("--repl", help="OUI Repl", action="store_true")
    args = arg_parser.parse_args()

    if args.repl:
        print("OUI Repl (Every line is a new execution environment)\ntype '.exit' to exit")
        running = True
        while running:
            code = str(input("> "))
            if code == ".exit": sys.exit(0)
            elif code.strip() == "": continue
            else:
                execute(code, welcome_text=False)
    elif args.file:
        execute(args.file.read())
        args.file.close()

# *drops mic*