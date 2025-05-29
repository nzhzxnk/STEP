import requests

# words.txtからsort済みwordと元のwordが対応するang_dictを作成
def create_ang_dict():
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

def create_counter_dict(ang_dict):
    counter_dict = {}
    for sort_word in ang_dict:
        each_dict={}
        # 空文字の場合
        if not sort_word:
            counter_dict[sort_word] = each_dict
            continue
        now = sort_word[0]
        count = 1
        for i in range(1,len(sort_word)):
            if now == sort_word[i]:
                count += 1
            else:
                each_dict[now] = count
                now = sort_word[i]
                count = 1
        each_dict[now] = count
        counter_dict[sort_word] = each_dict
    return counter_dict

def create_score_dict(counter_dict):
    score_map = {
        'a': 1, 'e': 1, 'h': 1, 'i': 1, 'n': 1, 'o': 1, 'r': 1, 's': 1, 't': 1,
        'c': 2, 'd': 2, 'l': 2, 'm': 2, 'u': 2,
        'b': 3, 'f': 3, 'g': 3, 'p': 3, 'v': 3, 'w': 3, 'y': 3,
        'j': 4, 'k': 4, 'q': 4, 'x': 4, 'z': 4
    }
    score_dict = {}
    for sort_word, each_dict in counter_dict.items():
        score = 0
        for char, num in each_dict.items():
            score += score_map.get(char, 0) * num 
            # mapから数を取ってくる。mapない文字は0点とする。
        score_dict[sort_word] = score
    return score_dict

# ang_dict = create_ang_dict()
# print("=== ang_dict ===")
# for i, k in enumerate(list(ang_dict)[:5]):
#     print(k, ":", ang_dict[k])

# counter_dict = create_counter_dict(ang_dict)
# print("\n=== counter_dict ===")
# for i, k in enumerate(list(counter_dict)[:5]):
#     print(k, ":", counter_dict[k])

# score_dict = create_score_dict(counter_dict)
# print("\n=== score_dict ===")
# for i, k in enumerate(list(score_dict)[:100]):
#     print(k, ":", score_dict[k])