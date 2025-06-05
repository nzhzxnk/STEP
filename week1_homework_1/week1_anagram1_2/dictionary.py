import requests

# words.txtからsort済みwordと元のwordが対応するang_listを作成
def create_list():
    ang_list = []
    # txtファイルをURLからダウンロードし、それぞれ処理してsort_wordとwordのang_listを作る
    response = requests.get("https://raw.githubusercontent.com/xharaken/step2/refs/heads/master/anagram/words.txt")
    lines = response.text.splitlines()
    for word in lines:
        word = word.strip()
        sort_word = "".join(sorted(word))
        # sort_wordと元のwordをタプルの形でang_listに保存していく
        ang_list.append((sort_word,word))
    # タプルの第一要素(sort_word)でang_listを並び替える
    ang_list.sort()
    return ang_list