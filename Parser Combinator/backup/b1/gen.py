from fun import Parser, letters, string, array_parser, choice, digits, many, sequence, sep_by, lazy, between

value_parser = lazy(lambda : choice(letters(), array, digits()))

array = array_parser(choice(string(', '), string(',')), value_parser)

# print(array.run('[a, b, c, [1,2,3], d]', 0))
parser = 
# (+ 1 4)