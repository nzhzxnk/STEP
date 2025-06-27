#!/usr/bin/env python3
import sys
import math
from queue import deque
from common import print_tour, read_input

def distance(city1_address, city2_address): # 2つの都市間のユークリッド距離を計算
    return math.sqrt((city1_address[0] - city2_address[0]) ** 2 + (city1_address[1] - city2_address[1]) ** 2) 

def calc_length(tour, address_list): # 与えられた訪問順序 tour に従って総経路長を計算
    n = len(address_list)  # nは都市の総数
    tour_length = 0
    for i in range(n):
        tour_length += distance(address_list[tour[i]], address_list[tour[(i + 1) % n]])
    return tour_length

# 初期の訪問経路を作成する(最近傍法:最も近い都市から訪れる貪欲法)
def solve(address_list): 
    n = len(address_list)
    # 既に訪問した都市を記録するためのセット
    visited_index = {0} # 最初の都市 (インデックス0) から開始
    tour = [0] # 訪問経路を格納するリスト

    # 未訪問の都市の中から最も近い都市を選択し、経路に追加
    for _ in range(1, n): # N-1回繰り返す
        current_city_index = tour[-1] # 現在いる都市のインデックス
        
        min_distance = float('inf') # 最小距離を無限大で初期化
        next_city_index = -1 # 次に訪問する都市のインデックス

        # 未訪問の都市の中から最も近い都市を探す
        for candidate_city_index in range(n):
            if candidate_city_index in visited_index:
                continue # 既に訪問済みの都市はスキップ
            
            # 現在の都市から候補の都市までの距離を計算
            d = distance(address_list[current_city_index], address_list[candidate_city_index])

            # 現在の最小距離よりも近ければ更新
            if d < min_distance:
                min_distance = d
                next_city_index = candidate_city_index
        
        # 最も近い都市を経路に追加し、訪問済みとする
        tour.append(next_city_index)
        visited_index.add(next_city_index)

    return tour # 最短経路の訪問順序を返す

# 2-optによる経路改善に、禁断探索法 (taboo Search)を組み合わせ実装
def taboo_search(tour, address_list, iteration_num, max_length_taboo):
    n = len(address_list)
    best_tour = tour[:] # 探索中に見つかった最良の経路を保存
    best_tour_length = calc_length(tour,address_list)# 探索中に見つかった最良の経路長を保存
    taboo_list = deque() # 最近訪れた都市を一定期間tabooリストにいれて、しばらく訪れないようにする。
                         # 探索済みの解にすぐ戻ってしまう (= 探索がループしてしまう) ことが少なくなることが期待される

    for i in range(iteration_num):
        best_change = float('inf') # その反復で最大の変化量を追跡する変数。無限大で初期化
        best_for_exchange_1, best_for_exchange_2 = -1, -1 # 最も改善が見込める交換を行う辺のインデックスを記録する変数
        
        # 交換による経路長の変化量を計算。負の値なら改善している（短くなる）
        for a in range(n):
            if tour[a] in taboo_list:
                continue
            for b in range(a + 2, n): # 2番目の辺の開始都市のインデックスbは、a+2 から n-1 まで
                if a == 0 and b == n - 1:  # a が最初の都市(0)で b が最後の都市(n-1)の場合はスキップ
                    continue
                old_two_edges_distance = distance(address_list[tour[a]], address_list[tour[(a + 1) % n]]) + distance( 
                    address_list[tour[b]], address_list[tour[(b + 1) % n]]
                ) # a=nの時など、a+1のままだとIndexerrorになってしまう。経路は巡回しているので、a=nのときa+1=1
                new_two_edges_distance = distance(address_list[tour[a]], address_list[tour[b]]) + distance(
                    address_list[tour[(a + 1) % n]], address_list[tour[(b + 1) % n]]
                )
                current_change = new_two_edges_distance - old_two_edges_distance
                if current_change < best_change:  # 交換による経路長の変化量 < best_changeの場合bestを更新
                    best_change = current_change
                    best_for_exchange_1, best_for_exchange_2 = a, b

        taboo_list.append(tour[best_for_exchange_1])
        if len(taboo_list) > max_length_taboo: #tabooリストのサイズが上限を超えた場合、最も古い要素を削除
            taboo_list.popleft()
        # 2-opt 交換を実行。tour[a_best + 1] から tour[b_best] までの部分を反転させる
        tour[best_for_exchange_1 + 1 : best_for_exchange_2 + 1] = tour[best_for_exchange_2:best_for_exchange_1:-1]

        current_length = calc_length(tour,address_list)
        if current_length < best_tour_length:
            best_tour_length = current_length
            best_tour = tour[:]
    return best_tour

if __name__ == '__main__':

    assert len(sys.argv) > 1 
    input_file_path = sys.argv[1]

    address_list = read_input(input_file_path) # 入力ファイルから座標を読み込む
    tour = solve(address_list) # 初期経路を取得
    iteration_num , max_length_taboo = 50, 5 #  iteration_numは改善を行う回数、max_length_tabooはタブーリストの大きさ、自分で決めれらる
    best_tour = taboo_search(tour, address_list, iteration_num, max_length_taboo)
    print_tour(best_tour)  # 結果の経路を出力