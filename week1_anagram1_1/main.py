# 計算量　O(n*mlogm+q*mlogm) 
# n:辞書の文字列(word)の数, m:文字列(word,string)の平均の長さ, q:クエリ数

# words.txtからsort済みwordと元のwordが対応するang_dictを作成:O(n*mlogm)
# 文字列の入力をstringで受け取り、ソートしてsort_stringを作成:O(q*mlogm)
# ang_dictにのkeyにsort_stringが含まれるかを探索する:O(q*1)
# 元のstring以外のanagramを出力する:O(q*7)(ang_dictのvalueの要素は最大で7つであった)

from dictionary import create_dict

def find_anagram(string,ang_dict):
    # 文字列(string)を入力し、strip()で余計なスペースや改行を取り除く
    # 辞書の時と同じようにソートしたsort_stringを作成する
    string = string.strip()
    sort_string = "".join(sorted(string))
    # ang_dictにのkeyにsort_stringが含まれるかを探索する
    count = 0
    ans = []
    if sort_string in ang_dict:
        ans_options = ang_dict[sort_string]
        for option in ans_options:
            # 元のstring以外のanagramを出力する
            if string != option:
                ans.append(option)
                count += 1
    return ans,count
    
def main():
    # sort_wordと元のwordを対応させた辞書(ang_dict)を作成する(dictionary.py内のcreate_dict関数を呼び出す)
    ang_dict = create_dict()
    string = input("文字列を入力してください: ") 
    ans,count = find_anagram(string,ang_dict)
    if count != 0:
        print(ans)
    # anagramが見つからなかった場合は"Not found"と表示
    else:
        print("Not found")

if __name__ == "__main__":
    main()