"""
OUI, The esolang that talks with you in a wierd way(s).

Written By Zoda:
	Links:
		- https://zoda-service.web.tr/code
		- https://github.com/kerem3338

Licensed under MIT license.

About The OUI
-	All Numbers are float's
-	Bools can be 'true', 'TT', 'false', 'FF'
-	Strings must be start and end with single quote
-	Operation (function)/variable names can include space or some special characters
-	OUI doesn't have super cow powers.

"""
import argparse
import random
import sys
import time

rnd_messages = [
	"Do you know you have rights?",
	"Try The D Programming Language.",
	"Who even reads that?",
	"*- 404 -*",
	"I hate everyone",
	"Good luck!",
	f"My lucky number is {random.randint(0,10)}",
	f"{'I hate you' if random.randint(0,1) == 1 else 'I don\' hate you'}"
]

holly_words = [
	"if", "i can", "make", "the",
	"world", "holly", "you", "can", "say",
	"what", "who is", "responsible", "to", "god", "good", "compiler", "witch", "tool", "a",
]

class Errors:
	var_not_founded = "variable not found! variable '{var}' not founded"
	unknown_operation = "unknown operation! '{operation}' is not recognized as a operation by OUI Commitie"
	argument_error = "argument error! '{location}' needs exactly {required} arguments, not {got}"
	var_value_error = "value error! '{e}' at '{location}' (variable name = '{var_name}')"
	value_error = "value error! '{e}' at '{location}'"

def get_number(src):
	return float(src)

def get_bool(src):
	if src in ["true","TT"]:
		return True
	elif src in ["false","FF"]:
		return False
	else: raise Exception("Invalid bool")

def get_string(src):
	_ = ""
	str_open = -1
	str_end  = -1
	for i,v in enumerate(src):
		if v == "'":
			if str_open != -1:
				str_end = i
			else:
				str_open = i
				continue

		if str_end == -1 and str_open != -1:
			_ += v

	return _

def get_from_type(inp, type):
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

def get_type_from_str(src):
	if len(src) >= 1:
		if src[0].isnumeric():
			return "number"
		else:
			if src in ["true","false","TT","FF"]:
				return "bool"
			else:
				return "string"
	raise Exception("source 'src' len must be at least 1")

def exact_arg_require(required, errors, got, location):
	if got != required:
		errors.append(Errors.argument_error.format(location = location, required = required, got = got))
		return False

	return True

def execute(src, welcome_text = True):
	if welcome_text:
		print(f'OUI Interpreter\n\nRandom message for you:\n\t{random.choice(rnd_messages)}\n')

	variables = {
		"propaganda": "I'm the selected programming language."
	}

	errors = []
	current = 0

	operations = []
	for op in src.split("---"):
		op = op.strip()
		if op == "": continue
		parts = [part for part in op.split("|") if part.strip() != ""]

		operations.append(parts)

	for op_i, op in enumerate(operations):
		match op[0]:
			case 'set-var':
				if not exact_arg_require(3, errors, len(op), 'set-variable'): continue
				
				var_name = get_string(op[1])
				try:
					variables[var_name] = get_from_type(op[2],get_type_from_str(op[2]))
				except Exception as e:
					errors.append(Errors.var_value_error.format(e=e, location="set-var", var_name = var_name))
			
			case 'do nothing for <x> amount of time':
				if not exact_arg_require(2, errors, len(op), 'set-variable'): continue

				
				try:
					wait_time = get_number(op[1])
				except Exception as e:
					errors.append(Errors.value_error.format(e=e, location="do nothing for <x> amout of time"))
					continue

				time.sleep(wait_time)

			case 'del-var':
				if not exact_arg_require(2, errors, len(op), 'set-variable'): continue
				var_name = get_string(op[1])

				if not var_name in variables:
						errors.append(Errors.var_not_founded.format(var=var_name))
						continue

				variables.pop(var_name)
				
			case 'print':
				for arg in op[1:]:
					print(get_string(arg))

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

			case 'where':
				print(op_i)
				
			case 'print_var':
				for arg in op[1:]:
					if not get_string(arg) in variables:
						errors.append(Errors.var_not_founded.format(var=get_string(arg)))
						continue
					print(variables[get_string(arg)])
			case _:
				errors.append(Errors.unknown_operation.format(operation=op[0]))

	print(f"\nExecution completed with ({len(errors)}) errors")
	for i, error in enumerate(errors):
		# You can't say 'FIX THE ERROR 0!' to someone... or if you can?
		print(f"\t├ {i + 1}) ", error)

if __name__ == "__main__":
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
