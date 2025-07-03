from collections import defaultdict

def count_char(string): # 文字列について出現する文字とその回数を保存
	component = defaultdict(int)
	for char in string:
		component[char] += 1
	return component

def calc_score(word): # 文字のスコアを計算
	word_score = 0
	char_score = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
	for char in word:
		word_score += char_score[ord(char)-ord('a')]
	return word_score

def find_best_word(words_list,string_component):
	for word,word_component,word_score in words_list:
		if can_create_anagram(string_component, word_component):
			return word
	return None

	# それぞれのcomponentの情報からanagramを作成できるか判定する
def can_create_anagram(string_component, word_component): 
	for char,num in word_component.items():
		if num > string_component[char]:
			return False
	return True

def import_file(filename): # ファイルを読み込みリストを作成
	import_words = []
	with open(filename) as f:
		for line in f:
			import_words.append(line.strip())
	return import_words

def create_words_list(): # word, word_component, scoreのリストを作成
	import_words = import_file("/Users/hayashiayano/Desktop/STEP/test_sample/words.txt")
	words_list = []
	for word in import_words:
		word_component = count_char(word)
		word_score = calc_score(word)
		words_list.append([word, word_component, word_score])
	return sorted(words_list,key = lambda x: x[2], reverse = True)

if __name__ == "__main__":
	import_strings = import_file("/Users/hayashiayano/Desktop/STEP/test_sample/small.txt") # 調べるstringをインポート
	words_list =  create_words_list() # 辞書からwordsをインポート
	output_list = []
	for string in import_strings:
		string_component = count_char(string)
		best_word = find_best_word(words_list,string_component)
		output_list.append(best_word)
	print(output_list)

	with open("/Users/hayashiayano/Desktop/STEP/test_sample/small_ans.txt", "w") as f:
		for word in output_list:
			f.write(word+"\n")

