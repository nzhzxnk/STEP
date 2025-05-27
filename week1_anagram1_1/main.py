from dictionary import create_dict

def find_anagram(string,ang_dict):
    # 辞書の時と同じようにソートしたsort_stringを作成する
    string = string.strip()
    sort_string = "".join(sorted(string))
    # angdictにstringが含まれるかを探索する
    # 元のstring以外のanagramを出力する
    count = 0
    ans = []
    if sort_string in ang_dict:
        ans_options = ang_dict[sort_string]
        for option in ans_options:
            if string != option:
                ans.append(option)
                count += 1
    return ans,count
    
def main():
    # sort_wordと元のwordを対応させた辞書(ang_dict)を作成する(dictionary.py内のcreate_dict関数を呼び出す)
    ang_dict = create_dict()
    # 文字列(string)を入力し、strip()で余計なスペースや改行を取り除く
    string = input("文字列を入力してください: ") 
    ans,count = find_anagram(string,ang_dict)
    if count != 0:
        print(ans)
    else:
        print("Not found")

if __name__ == "__main__":
    main()