import copy
import sys

path = 'wiki-100k.txt'


# open a text file that contains english words on each line
# then make the words a key to a dictionary
def makeWordDictionary(path):
	words_dictionary = {}
	with open(path,'r', encoding='utf8') as f:
		lines = f.readlines()
		# each line only contains a word
		for line in lines:
			if line[:2] != '#!':
				for word in line.split():
					words_dictionary[word.lower()] = None
		f.close()
	return words_dictionary

# generate all the possible combination of characters on a given list
def genCombination(char_list):
	assert len(char_list) < 11
	if len(char_list) == 1: return char_list
	result = []
	for char in char_list:
		char_list_copy = copy.copy(char_list)
		char_list_copy.remove(char)
		for pre_result in genCombination(char_list_copy):
			result.append(str(char)+pre_result)
	return result

# get the last n characters of all the elements of the list
# assuming the list only contains string of equal length
def getLastChars(possible_combinations, n):
	n_char_word = []
	for word in possible_combinations:
		n_char_word.append(word[-n:])
	return n_char_word



def main(argv):
	done = False
	words_dictionary = makeWordDictionary(path)
	while not done:
		# get the possible characters
		chars = list(input("chars: "))
		# get all the posible len(chars) letter combination
		all_combinations = genCombination(chars)
		# extract all the posible n letter combination of characters
		# from all combinations
		for n in range(3, len(chars)+1):
			print(f'{n} letter words')
			# get the n letter combinations
			n_char_combination = getLastChars(all_combinations, n)
			n_char_combination_in_dict = []
			# print all combinations that is on the dictionary
			for word in n_char_combination:
				if word in words_dictionary and word not in n_char_combination_in_dict: n_char_combination_in_dict.append(word)
			print(n_char_combination_in_dict)
		flag = input("again:[y/n]")
		if flag == 'n': done = True
		print("__________________________________________________________________")




if __name__ == '__main__':
	main(sys.argv)
