# counter関数を使わずに実装した例
# ang_dictを元に、score_dict(sort_wordとword_score),counter_dict(sort_word,word_counter)を作成
# dictがソート済みであることを利用し,forで各要素の種類と数を計上しcounter_dictを作成
# 入力(string)を受け取りソートして、string_counterを作成
# string_counterとword_counterの差分がFalseかつword_scoreが最大のものを出力

from dictionary import create_ang_dict
from dictionary import create_counter_dict
from dictionary import create_score_dict
import requests

# 本体となるfind_max_anagram関数
def find_max_anagram(string,ang_dict,counter_dict,score_dict):
    string = string.strip()
    # 入力(string)を受け取りソートして、string_counterを作成
    string_counter_dict = string_counter(string)
    # substring_checkがTrue(部分文字列から作成可能)かつword_scoreが最大となるsort_wordを出力
    max_score = 0
    max_score_word = None
    for sort_word,required in counter_dict.items():
        if substring_check(string_counter_dict,required):
            if max_score < score_dict[sort_word]:
                max_score = score_dict[sort_word]
                max_score_word = sort_word
    # 元のstringと同じものがあっても排除しないことにする
    return ang_dict[max_score_word]

# 入力(string)を受け取りソートして、string_counter_dict(含まれている文字の種類と数を対応させた辞書)を作成
def string_counter(string):
    sort_string = "".join(sorted(string))
    string_counter_dict={}
    now = None
    count = 0
    for i in range(len(sort_string)):
        if now == sort_string[i]:
            count += 1
        else:
            if not now:
                string_counter_dict[now] = count
                now = sort_string[i]
                count = 1
    string_counter_dict[now] = count
    return string_counter_dict

# string_counter_dictとrequired(counter_dictのそれぞれのwordに対しての辞書)を比べ、stringの部分文字列でwordを作れるか判定
def substring_check(string_counter_dict,required):
    for char,num in required.items(): 
        if string_counter_dict.get(char,0) < num:
            return False
    return True

# stringを1クエリとして扱いfin_max_anagram関数を実行
def main(link):
    # ang_dictを元に、score_dict(sort_wordとword_score),counter_dict(sort_word,word_counter)を作成
    ang_dict = create_ang_dict()
    counter_dict = create_counter_dict(ang_dict)
    score_dict = create_score_dict(counter_dict)
    # linkから入力を受け取る
    response = requests.get(link)
    lines = response.text.splitlines()
    for string in lines:
        print(find_max_anagram(string,ang_dict,counter_dict,score_dict))

if __name__ == "__main__":
    main("https://github.com/xharaken/step2/blob/master/anagram/small.txt")
    # main("https://github.com/xharaken/step2/blob/master/anagram/medium.txt")
    # main("https://github.com/xharaken/step2/blob/master/anagram/large.txt")

