#計算量：
# 
# counter関数を使わずに実装した例
# ang_dictを元に、score_dict(sort_wordとword_score),counter_dict(sort_word,word_counter)を作成:
# dictがソート済みであることを利用し,forで各要素の種類と数を計上しcounter_dictを作成
# 入力(string)を受け取りソートして、string_counterを作成
# string_counterとword_counterの差分がFalseかつword_scoreが最大のものを出力

from dictionary import create_ang_dict
from dictionary import create_counter_dict
from dictionary import create_score_dict
from other import string_counter
from other import substring_check
import requests

# 本体となるfind_max_anagram関数
def find_max_anagram(string,ang_dict,counter_dict,score_dict):
    string = string.strip()
    # 入力(string)を受け取りソートして、string_counte_dictrを作成
    string_counter_dict = string_counter(string)
    # substring_checkがTrue(部分文字列から作成可能)かつword_scoreが最大となるsort_wordを出力
    max_score = -1
    max_score_word = None
    for sort_word,required in counter_dict.items():
        if substring_check(string_counter_dict,required):
            # 元のstringと同じものであれば排除する
            # ang_dict[sort_word] はリストなので、stringがそのリストに含まれているかチェック
            # かつ、そのsort_wordに対応するアナグラムが元のstringしかない場合
            # 元のstringしかアナグラムがない場合はスキップ
            if string in ang_dict[sort_word] and len(ang_dict[sort_word]) == 1:
                continue
            current_score = score_dict.get(sort_word, 0) # score_dictにない場合も考慮
            if max_score_word is None or current_score > max_score: # max_score_wordがNoneの場合の初期化
                max_score = current_score
                max_score_word = sort_word
    if max_score_word:
        return ang_dict[max_score_word][0]
    else:
        return None

# stringを1クエリとして扱いfin_max_anagram関数を実行
def main(link,output_filename="output.txt"):
    # ang_dictを元に、score_dict(sort_wordとword_score),counter_dict(sort_word,word_counter)を作成
    ang_dict = create_ang_dict()
    counter_dict = create_counter_dict(ang_dict)
    score_dict = create_score_dict(counter_dict)
    # linkから入力を受け取る
    response = requests.get(link)
    lines = response.text.splitlines()
    # ファイル書き込みのためにopen関数を使用
    with open(output_filename, 'w', encoding='utf-8') as f:
        for string in lines:
            result = find_max_anagram(string, ang_dict, counter_dict, score_dict)
            if result:
                f.write(result + '\n')
            else:
                f.write("\n") # 見つからなかった場合は空行を出力

if __name__ == "__main__":
    main("https://raw.githubusercontent.com/xharaken/step2/refs/heads/master/anagram/small.txt","small_answer.txt")
    # main("https://raw.githubusercontent.com/xharaken/step2/refs/heads/master/anagram/medium.txt","medium_answer.txt")
    # main("https://raw.githubusercontent.com/xharaken/step2/refs/heads/master/anagram/large.txt","large_answer.txt")

