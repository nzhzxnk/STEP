# 計算量　O(n*mlogm+q*mlogm) 
# n:辞書の文字列(word)の数, m:文字列(word,string)の平均の長さ, q:クエリ数

# words.txtからsort済みwordと元のwordをタプルにしたang_listを作成:O(n*mlogm+nlogn)
# 文字列の入力をstringで受け取り、ソートしてsort_stringを作成:O(q*mlogm)
# ソート順になっているang_listを二分探索し、sort_stringがang_listにあった場合に入る場所をインデックスで返す:O(q*logn)
# ang_listのタプル第一要素(sort_word)がsort_stringと一致する間のみ探索を続け、そのうち第二要素(word)がstringと一致しないもののみを出力する:O(q*7)(anagram同士である辞書内の要素は最大で7つであった)

from dictionary import create_list
from search import binary_search

def find_anagram(string,ang_list):
    # 文字列(string)を入力し、strip()で余計なスペースや改行を取り除く
    # 辞書の時と同じようにソートしたsort_stringを作成する
    string = string.strip()
    sort_string = "".join(sorted(string))
    # ソート順になっているang_listを二分探索し、sort_stringがang_listにあった場合に入る場所をインデックスで返す
    i = binary_search(ang_list,sort_string)
    count = 0
    ans = []
    # 二分探索では入りうる場所を考えただけなので、ang_list内にsort_stringが存在するとは限らない
    # ang_listのタプル第一要素がsort_stringと一致し、第二要素がstringと一致しないもののみを出力する
    while ang_list[i][0] == sort_string:
        if ang_list[i][1] != string:
            ans.append(ang_list[i][1])
            count += 1
        i += 1
    return ans,count

def main():
    # sort_wordと元のwordを対応させたリスト(ang_list)を作成する(dictionary.py内のcreate_list関数を呼び出す)
    ang_list = create_list()
    string = input("文字列を入力してください: ") 
    ans,count = find_anagram(string,ang_list)
    if count != 0:
        print(ans)
    
    else:
        print("Not found")

if __name__ == "__main__":
    main()