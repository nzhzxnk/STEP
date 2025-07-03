from collections import defaultdict
import re

def init_components(sequence: list) -> tuple[defaultdict, defaultdict]:
    left_component = defaultdict(int)
    right_component = defaultdict(int)

    # right_component をシーケンス全体のGとWの数で初期化
    right_component["G"] = sequence.count("G")
    right_component["W"] = sequence.count("W")

    return left_component, right_component

def calc_replacement(left_comp: defaultdict, right_comp: defaultdict) -> int:
    return left_comp["W"] + right_comp["G"]

# --- メイン処理 ---
if __name__ == '__main__':
    input_line = input().strip()
    string_sequence = re.split(r'[,]', input_line) # ここで文字列のリストになります
    is_valid_input = True
    for char in string_sequence:
        if not char in ("W","G"):
            is_valid_input = False
    if is_valid_input:
        # 初期化: 境界が一番左にある状態
        left_component, right_component = init_components(string_sequence)

        # 最初の置換回数を最小値として設定
        min_replacement = calc_replacement(left_component, right_component)

        # 境界を右に1文字ずつずらしながらcomponentを更新し、最小置換回数を探索
        for char in string_sequence:
            # 境界がcharを通過する。charはright_componentからleft_componentへ移動する。
            if right_component[char] > 0: # 念のため、right_componentにcharがあることを確認
                right_component[char] -= 1 # rightから減らす
                left_component[char] += 1   # leftへ増やす
            # 新しい境界での置換回数を計算
            current_replacement = calc_replacement(left_component, right_component)

            # 最小値を更新
            if current_replacement < min_replacement:
                min_replacement = current_replacement

        # 最終的な最小置換回数を出力
        print(min_replacement)
    else:
        print("Valueerror")