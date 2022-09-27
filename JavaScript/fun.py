class Parser():
	def __init__(self, transformFn):
		self.transformFn = transformFn

	def run(self, targetStr, index):
		return self.transformFn(targetStr, index)

	def map(self, fn):
		def ntfn(targetStr, index):
			result = self.transformFn(targetStr, index)
			return fn(result)
		return Parser(ntfn)

	def chain(self, parser):
		def ntfn(targetStr, index):
			result = {
				'isError': False,
				'result': None,
				'error': None,
				'index': 0
			}
			current_parser_result = self.transformFn(targetStr, index)
			if not current_parser_result['isError']:
				parser_result = parser.run(targetStr, current_parser_result['index'])
				if not parser_result['isError']:
					result["isError"] = False
					result["result"] = [current_parser_result["result"], parser_result["result"]]
					result["index"] = parser_result["index"]
				else:
					result = parser_result
			else:
				result = current_parser_result

			return result
		return Parser(ntfn)

def str(s):
	def transformFn(targetStr, index=0):
		result = {
			'isError': False,
			'result': None,
			'error': None,
			'index': 0
		}
		# startIndex = targetStr.find(s, index)
		if targetStr.startswith(s, index):
			result['result'] = s
			result['index'] = index+len(s)
		else:
			result['isError'] = True
			result['error'] = f'str: tried to much {s}, instead got {targetStr[index:index+10]}'
			result['index'] = index
		return result
	return transformFn

def f(result):
	result["result"] = result["result"].upper()
	return result

worldParser = Parser(str("world"))
helloParser = Parser(str("hello")).chain(worldParser)

print(helloParser.run("helloworld", 0))
# print(worldParser.run("world", 0))
