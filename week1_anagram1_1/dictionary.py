import requests

# words.txtからsort済みwordと元のwordが対応するang_dictを作成
def create_dict():
    ang_dict = {}
    # txtファイルをURLからダウンロードし、それぞれ処理してsort_wordとwordの辞書を作る
    response = requests.get("https://raw.githubusercontent.com/xharaken/step2/refs/heads/master/anagram/words.txt")
    lines = response.text.splitlines()
    for word in lines:
        word = word.strip()
        sort_word = "".join(sorted(word))
        # 辞書の中にもanagram同士が存在し、keyが被る可能性があるのでvalueはlist形式で保存する
        if sort_word in ang_dict:
            ang_dict[sort_word].append(word)
        else:
            ang_dict[sort_word] = [word]
    return ang_dict
