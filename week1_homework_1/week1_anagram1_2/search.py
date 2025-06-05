# ソート順になっているang_listを二分探索し、sort_stringがang_listにあった場合に入る場所をインデックスで返す
def binary_search(ang_list,sort_string):
    left = 0
    right = len(ang_list)
    # sort_string以降にある文字列のインデックスの最小値を求める
    while left < right:
        mid = (left+right)//2
        if ang_list[mid][0] >= sort_string:
            right = mid
        else:
            left = mid+1
    return left