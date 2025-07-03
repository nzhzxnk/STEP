import sys
import math
from collections import deque
from common import read_input, print_tour

def distance(city1_index, city2_index): # 2つの都市のindexから距離を求める
    city1_address = address_dict[city1_index] # address_dictを使用し、indexからaddressを取得する
    city2_address = address_dict[city2_index]
    # 2都市間のユーグリット距離を求める
    return math.sqrt((city1_address[0] - city2_address[0]) ** 2 + (city1_address[1] - city2_address[1]) ** 2)

def calc_length_in_zone(tour_in_zone): # tourの巡回路の長さを計算する
    n = len(tour_in_zone)
    tour_length = 0
    for i in range(n):  # tourの巡回順に長さを調べ加えていく
        tour_length += distance(tour_in_zone[i], tour_in_zone[(i+1)%n])
    return tour_length

def calc_zone_range(address_list): # 各inputに含まれる全都市のx,y座標の範囲を計算する
    if not address_list: # inputに都市が含まれない場合は、xの最小値・最大値、yの最小値・最大値すべて0
        return 0, 0, 0, 0
    # 全都市のx座標/y座標のみをリスト化しソートする
    x_address_list = sorted([address_list[i][0] for i in range(len(address_list))])
    y_address_list = sorted([address_list[i][1] for i in range(len(address_list))])
    min_x, max_x = x_address_list[0], x_address_list[-1]
    min_y, max_y = y_address_list[0], y_address_list[-1]
    return min_x, max_x, min_y, max_y # xの最小値・最大値、yの最小値・最大値を決定する

def divide_city_in_zone(address_list, num_rows=2, num_cols=3): # 都市全体を2行3列の6ゾーンに分割する
    min_x, max_x, min_y, max_y = calc_zone_range(address_list) # 各inputに含まれる全都市のx,y座標の範囲を計算する
    # x,yの範囲が0の場合（すべて同じ場合や都市が0の場合）は回避
    x_step = (max_x - min_x) / num_cols if (max_x - min_x) > 0 else 1.0
    y_step = (max_y - min_y) / num_rows if (max_y - min_y) > 0 else 1.0 

    divided_index_list = [[[] for _ in range(num_cols)] for _ in range(num_rows)] # ゾーンごとに都市のindexをリストに保存
    for index, (city_x, city_y) in enumerate(address_list):
        zone_x = 0
        if (max_x - min_x) > 0:
            zone_x = int((city_x - min_x) // x_step)
            if zone_x == num_cols: # 最大値が最後のゾーンから溢れてindexerrorにならないように調整
                zone_x = num_cols - 1
        zone_y = 0
        if (max_y - min_y) > 0:
            zone_y = int((city_y - min_y) // y_step)
            if zone_y == num_rows:  # 最大値が最後のゾーンから溢れてindexerrorにならないように調整
                zone_y = num_rows - 1
        divided_index_list[zone_y][zone_x].append(index)
    return divided_index_list

# 各ゾーンにおける初期の訪問経路を作成する(最近傍法:最も近い都市から訪れる貪欲法)
def solve_in_zone(index_list_in_zone): 
    n = len(index_list_in_zone)
    if n == 0:
        return []
    # 既に訪問した都市を記録するためのセット
    visited_index = {index_list_in_zone[0]} # index_list_in_zoneの最初のindexから開始
    tour_in_zone = [index_list_in_zone[0]] # 訪問経路を格納するリスト

    # 未訪問の都市の中から最も近い都市を選択し、経路に追加
    for _ in range(1, n): # n-1回繰り返す
        current_city_index = tour_in_zone[-1] # 現在いる都市のインデックス
        min_distance = float('inf') # 最小距離を無限大で初期化
        next_city_index = -1 # 次に訪問する都市のインデックス
        # 未訪問の都市の中から最も近い都市を探す
        for candidate_city_index in index_list_in_zone:
            if candidate_city_index in visited_index:
                continue # 既に訪問済みの都市はスキップ
            d = distance(current_city_index, candidate_city_index) # 現在の都市から候補の都市までの距離を計算
            if d < min_distance: # 現在の最小距離よりも近ければ更新
                min_distance = d
                next_city_index = candidate_city_index
        # 最も近い都市を経路に追加し、訪問済みとする
        tour_in_zone.append(next_city_index)
        visited_index.add(next_city_index)
    return tour_in_zone # 最短経路の訪問順序を返す

# 各ゾーンにおける2-opt, 禁断探索法 (taboo Search) による経路改善を行う
def taboo_search_in_zone(tour_in_zone, index_list_in_zone, iteration_num=750, max_length_taboo=20):
    n = len(tour_in_zone)
    best_tour_in_zone = tour_in_zone[:] # 探索中に見つかった最良の経路を保存
    best_tour_length = calc_length_in_zone(tour_in_zone)# 探索中に見つかった最良の経路長を保存
    taboo_list = deque() # 最近訪れた都市を一定期間tabooリストにいれて、しばらく訪れないようにする。
                         # 探索済みの解にすぐ戻ってしまう (= 探索がループしてしまう) ことが少なくなることが期待される

    for i in range(iteration_num):
        best_change = float('inf') # その反復で最大の変化量を追跡する変数。無限大で初期化
        best_for_exchange_1, best_for_exchange_2 = -1, -1 # 最も改善が見込める交換を行う辺のインデックスを記録する変数
        # 交換による経路長の変化量を計算。負の値なら改善している（短くなる）
        for a in range(n):
            if tour_in_zone[a] in taboo_list:
                continue
            for b in range(a+2, n): # 2番目の辺の開始都市のインデックスbは、a+2 から n-1 まで
                if a == 0 and b == n - 1:  # a が最初の都市(0)で b が最後の都市(n-1)の場合はスキップ
                    continue
                old_two_edges_distance = distance(tour_in_zone[a], tour_in_zone[(a+1) % n]) + distance( 
                    tour_in_zone[b],tour_in_zone[(b + 1) % n]
                ) # a=nの時など、a+1のままだとIndexerrorになってしまう。経路は巡回しているので、a=nのときa+1=1
                new_two_edges_distance = distance(tour_in_zone[a], tour_in_zone[b]) + distance(
                    tour_in_zone[(a + 1) % n], tour_in_zone[(b + 1) % n]
                )
                current_change = new_two_edges_distance - old_two_edges_distance
                if current_change < best_change:  # 交換による経路長の変化量 < best_changeの場合bestを更新
                    best_change = current_change
                    best_for_exchange_1, best_for_exchange_2 = a, b

        taboo_list.append(tour_in_zone[best_for_exchange_1])
        if len(taboo_list) > max_length_taboo: #tabooリストのサイズが上限を超えた場合、最も古い要素を削除
            taboo_list.popleft()
        # 2-opt交換を実行。tour[a_best + 1] から tour[b_best] までの部分を反転させる
        tour_in_zone[best_for_exchange_1 + 1 : best_for_exchange_2 + 1] = tour_in_zone[best_for_exchange_2:best_for_exchange_1:-1]
        current_length = calc_length_in_zone(tour_in_zone)
        if current_length < best_tour_length:
            best_tour_length = current_length
            best_tour_in_zone = tour_in_zone[:]
    return best_tour_in_zone

# 各ゾーンにおける最短の巡回路を計算し、それらを繋げゾーンを時計回りに訪問していく時の全体での最短順回路を求める
def conbine_best_tours(divided_index_list):
    zone_order = [(0,0),(0,1),(0,2),(1,2),(1,1),(1,0)] 
    final_best_tour = [] # 最終的な結合された経路 (ノードの元のインデックス)
    for r, c in zone_order: # ゾーンを時計回り順に訪問していく (0,0) -> (0,1) -> (0,2) -> (1,2) -> (1,1) -> (1,0)
        index_list_in_zone = divided_index_list[r][c]
        if not index_list_in_zone: # このゾーンにノードがない場合はスキップ
            continue
        tour_in_zone = solve_in_zone(index_list_in_zone) # ゾーン内TSPの初期経路を最近傍法で計算
        best_tour_in_zone = taboo_search_in_zone(tour_in_zone, index_list_in_zone) # 2-optとタブーサーチで経路を改善
        final_best_tour.extend(best_tour_in_zone) # 計算した各ゾーンにおける最短経路を、全体の経路に追加する
    return final_best_tour

if __name__ == '__main__':
    assert len(sys.argv) > 1 
    input_file_path = sys.argv[1]
    address_list = read_input(input_file_path) # 入力ファイルから座標を読み込む
    address_dict = {} # indexからaddressを取得するaddress_dictを作成する
    for index,address in enumerate(address_list):
        address_dict[index] = address
    divided_index_list = divide_city_in_zone(address_list) # 都市全体を2行3列の6ゾーンに分割する
    # 各ゾーンにおける最短の巡回路を計算し、それらを繋げゾーンを時計回りに訪問していく時の全体での最短順回路を求める
    final_best_tour = conbine_best_tours(divided_index_list) 
    print_tour(final_best_tour) # 結果の経路を出力