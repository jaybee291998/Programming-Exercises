from fun import *

value_parser = lazy(lambda : choice(letters(), array, digits()))

array = array_parser(choice(string(', '), string(',')), value_parser)

def format_output(result):
	result_list = result["result"]
	new_result = {
		"type": None,
		"a": None,
		"b": None
	}
	if result_list[0] == '+': new_result["type"] = 'ADD'
	elif result_list[0] == '-': new_result["type"] = 'SUB'
	elif result_list[0] == '*': new_result["type"] = 'MUL'
	elif result_list[0] == '/': new_result["type"] = 'DIV'
	else 

	new_result["a"] = result_list[1]
	new_result["b"] = result_list[2]

	result["result"] = [new_result]
	return result

# print(array.run('[a, b, c, [1,2,3], d]', 0))
between_bracket = between(string('('), string(')'))
space = string(' ')
value_parser = lazy(lambda : choice(digits(), parser))
parser = between_bracket(sequence(
	choice(string('+'), string('-'), string('*'), string('/'), string('')),
	space,
	value_parser,
	space,
	value_parser
	)).map(remove_bracket).map(remove_specific_item(' ')).map(format_output)
# (+ 1 4)

print(parser.run("(+ (/ (- 1 5) (* 5 (+ 5 8))) (* 5 6))", 0))



