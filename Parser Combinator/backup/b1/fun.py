class Parser():
	def __init__(self, transformFn):
		self.transformFn = transformFn

	def run(self, targetStr, index):
		return self.transformFn(targetStr, index)

	def map(self, fn):
		def ntfn(targetStr, index):
			result = self.transformFn(targetStr, index)
			if result["isError"]: return result
			return fn(result)
		return Parser(ntfn)

	def chain(self, fn):
		def ntfn(targetStr, index):
			result = self.transformFn(targetStr, index)
			if result["isError"]: return result
			parser = fn(result)	# the parser based on the fn
			parser_result = parser.run(targetStr, index + result["index"])

			result["result"].extend(parser_result["result"])
			parser_result["result"] = result["result"]

			return parser_result
		return Parser(ntfn)

def string(s):
	def transformFn(targetStr, index=0):
		result = {
			'isError': False,
			'result': [],
			'error': None,
			'index': index
		}
		# startIndex = targetStr.find(s, index)
		if targetStr.startswith(s, index):
			result['result'].append(s)
			result['index'] = index+len(s)
		else:
			result['isError'] = True
			result['error'] = f'str: tried to much {s}, instead got {targetStr[index:index+10]}'
			result['index'] = index
		return result
	return Parser(transformFn)

def letters():
	def transformFn(targetStr, index=0):
		result = {
			'isError': False,
			'result': [],
			'error': None,
			'index': index
		}
		res = ''
		for char in targetStr[index:]:
			if not char.isalpha(): break
			res += char
		if len(res) > 0:
			result["result"].append(res)
			result["index"] = index + len(res)
		else:
			result["isError"] = True 
			result["error"] = f'letters: no letters found in "{targetStr[index:]}" @{index}'

		return result
	return Parser(transformFn)

def digits():
	def transformFn(targetStr, index=0):
		result = {
			'isError': False,
			'result': [],
			'error': None,
			'index': index
		}
		res = ''
		for char in targetStr[index:]:
			if not char.isdigit(): break
			res += char
		if len(res) > 0:
			result["result"].append(int(res))
			result["index"] = index + len(res)
		else:
			result["isError"] = True 
			result["error"] = f'digits: no digits found in "{targetStr[index:]}" @{index}'


		return result
	return Parser(transformFn)

def sequence(*args):
	parsers = args
	def transformFn(targetStr, index):
		result = {
			'isError': False,
			'result': [],
			'error': None,
			'index': index
		}
		current_index = index
		for parser in parsers:
			res = parser.run(targetStr, current_index)
			if not res["isError"]:
				result["result"].extend(res["result"])
				current_index = res["index"]
			else:
				break
		if len(result["result"]) > 0:
			result["index"] = current_index
		else:
			result["isError"] = True 
			result["error"] = f'sequence: no parser can parse {targetStr}'
		return result
	return Parser(transformFn)

def choice(*args):
	parsers = args
	def transformFn(targetStr, index):
		result = {
			'isError': False,
			'result': [],
			'error': None,
			'index': index
		}
		for parser in parsers:
			res = parser.run(targetStr, index)
			if not res["isError"]:
				return res
		result["isError"] = True
		result["error"] = f'choice: no parser match the {targetStr[index:]}'
		return result

	return Parser(transformFn)

def many(parser):
	def transformFn(targetStr, index):
		result = {
			'isError': False,
			'result': [],
			'error': None,
			'index': index
		}
		done = False 
		current_index = index
		while not done:
			res = parser.run(targetStr, current_index)
			if not res["isError"]: 
				result["result"].extend(res["result"])
				current_index = res["index"]
			else:
				done = True 

		if len(result["result"]) <= 0:
			result["isError"] = True 
			result["error"] = f'many: cant match parser with {targetStr[index:]}'
		else:
			result["index"] = current_index

		return result

	return Parser(transformFn)

def sep_by(seperator_parser, value_parser):
	def ntfn(targetStr, index):
		result = {
			'isError': False,
			'result': [],
			'error': None,
			'index': index
		}
		results = []
		current_index = index;
		while True:
			value_parser_result = value_parser.run(targetStr, current_index)
			if value_parser_result["isError"]: break
			current_index = value_parser_result["index"]

			results.extend(value_parser_result["result"])

			seperator_parser_result = seperator_parser.run(targetStr, current_index)
			if seperator_parser_result["isError"]: break
			current_index = seperator_parser_result["index"]

		result["result"].append(results)
		result["index"] = current_index
		return result
	return Parser(ntfn)

def between(left_parser, rigth_parser):
	def n(content_parser):
		return sequence(
			left_parser,
			content_parser,
			rigth_parser
			)
	return n

def array_parser(seperator_parser, initial_value_parser):
	def remove_bracket(result):
		del result["result"][0]
		result["result"].pop()
		return result

	def transformFn(targetStr, index):
		# value_parser = lazy(lambda : choice([initial_value_parser]))
		bracket_parser = between(string('['), string(']'))
		return bracket_parser(sep_by(seperator_parser, initial_value_parser)).map(remove_bracket).run(targetStr, index)
	return Parser(transformFn)

def lazy(parser_thunk):
	def transformFn(targetStr, index):
		parser = parser_thunk()
		return parser.transformFn(targetStr, index)
	return Parser(transformFn)

