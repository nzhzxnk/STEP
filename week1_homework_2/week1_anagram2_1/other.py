
# 入力(string)を受け取りソートして、string_counter_dict(含まれている文字の種類と数を対応させた辞書)を作成
def string_counter(string):
    sort_string = "".join(sorted(string))
    string_counter_dict={}
    if not sort_string: # 空文字列の場合のハンドリング
        return string_counter_dict
    now = sort_string[0]
    count = 1
    for i in range(1,len(sort_string)):
        if now == sort_string[i]:
            count += 1
        else:
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