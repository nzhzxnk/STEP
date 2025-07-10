import sys
import math
from collections import deque
from common import read_input, print_tour

class TravelingSalesman: # col,rowの数はどのインスタンスでも共通なのでクラス変数とする
    num_cols = 2
    num_rows = 3
    max_length_taboo = 20

    def __init__(self): # 各インスタンスごとにaddress_listなどは変化するのでインスタンス変数
        self.address_list = []
        self.address_dict = {} # indexからaddressを取得するaddress_dictを作成する
        self.divided_index_list = [[[] for _ in range(TravelingSalesman.num_cols)] for _ in range(TravelingSalesman.num_rows)] # ゾーンごとに都市のindexをリストに保存
        print(self.divided_index_list)

    def distance(self,city1_index, city2_index): # 2つの都市のindexから距離を求める
        city1_address = self.address_dict[city1_index] # address_dictを使用し、indexからaddressを取得する
        city2_address = self.address_dict[city2_index]
        # 2都市間のユーグリット距離を求める
        return math.sqrt((city1_address[0] - city2_address[0]) ** 2 + (city1_address[1] - city2_address[1]) ** 2)

    def calc_length_in_zone(self, tour): # tourの開始点から終了点までの長さを計算する
        tour_length = 0
        prev_city_index = None
        for city_index in tour: # tourの訪問順に長さを調べ加えていく
            if prev_city_index is not None:
                tour_length += self.distance(city_index,prev_city_index)
            prev_city_index = city_index
        return tour_length

    def calc_zone_range(self): # 各inputに含まれる全都市のx,y座標の範囲を計算する
        if not self.address_list: # inputに都市が含まれない場合は、xの最小値・最大値、yの最小値・最大値すべて0
            return 0, 0, 0, 0
        # 全都市のxの最小値・最大値、yの最小値・最大値を決定する
        min_x, min_y = self.address_list[0]
        max_x, max_y = min_x, min_y
        for point in self.address_list:
            min_x = min(point[0],min_x)
            max_x = max(point[0],max_x)
            min_y = min(point[1],min_y) 
            max_y = max(point[1],max_y) 
            # print(f"point: {point}")
            # print(f"min_x, max_x, min_y, max_y: {min_x, max_x, min_y, max_y}")
        return min_x, max_x, min_y, max_y 

    def divide_city_in_zone(self): # 都市全体を2行3列の6ゾーンに分割する
        min_x, max_x, min_y, max_y = self.calc_zone_range() # 各inputに含まれる全都市のx,y座標の範囲を計算する
        # x,yの範囲が0の場合（すべて同じ場合や都市が0の場合）は回避
        x_step = (max_x - min_x) / TravelingSalesman.num_cols if (max_x - min_x) > 0 else 1.0
        y_step = (max_y - min_y) / TravelingSalesman.num_rows if (max_y - min_y) > 0 else 1.0 
        # print(f"min_x, max_x, min_y, max_y: {min_x, max_x, min_y, max_y}")
        for index, (city_x, city_y) in enumerate(self.address_list):
            zone_x = 0
            if (max_x - min_x) > 0:
                # print(f"city_x,min_x,x_step: {city_x,min_x,x_step}")
                zone_x = int((city_x - min_x) // x_step)
                # print(zone_x)
                if zone_x == TravelingSalesman.num_cols: # 最大値が最後のゾーンから溢れてindexerrorにならないように調整
                    zone_x = TravelingSalesman.num_cols - 1
                    # print(f"zone_x: {zone_x}")
            zone_y = 0
            if (max_y - min_y) > 0:
                zone_y = int((city_y - min_y) // y_step)
                if zone_y == TravelingSalesman.num_rows:  # 最大値が最後のゾーンから溢れてindexerrorにならないように調整
                    zone_y = TravelingSalesman.num_rows - 1
            self.divided_index_list[zone_y][zone_x].append(index)

    # 各ゾーンにおける初期の訪問経路を作成する(最近傍法:最も近い都市から訪れる貪欲法)
    def solve_in_zone(self, index_list): 
        n = len(index_list)
        if n == 0:
            return []
        # 既に訪問した都市を記録するためのセット
        visited_index = {index_list[0]} # index_listの最初のindexから開始
        tour = [index_list[0]] # 訪問経路を格納するリスト

        # 未訪問の都市の中から最も近い都市を選択し、経路に追加
        for _ in range(1, n): # n-1回繰り返す
            curr_city_index = tour[-1] # 現在いる都市のインデックス
            min_distance = float('inf') # 最小距離を無限大で初期化
            next_city_index = -1 # 次に訪問する都市のインデックス
            # 未訪問の都市の中から最も近い都市を探す
            for candidate_city_index in index_list:
                if candidate_city_index in visited_index:
                    continue # 既に訪問済みの都市はスキップ
                d = self.distance(curr_city_index, candidate_city_index) # 現在の都市から候補の都市までの距離を計算
                if d < min_distance: # 現在の最小距離よりも近ければ更新
                    min_distance = d
                    next_city_index = candidate_city_index
            # 最も近い都市を経路に追加し、訪問済みとする
            tour.append(next_city_index)
            visited_index.add(next_city_index)
        return tour # 最短経路の訪問順序を返す

    # 各ゾーンにおける2-opt, 禁断探索法 (taboo Search) による経路改善を行う
    def taboo_search_in_zone(self, tour, iteration_num =500):
        n = len(tour)
        best_tour = tour[:] # 探索中に見つかった最良の経路を保存
        best_tour_length = self.calc_length_in_zone(tour)# 探索中に見つかった最良の経路長を保存
        taboo_list = deque() # 最近訪れた都市を一定期間tabooリストにいれて、しばらく訪れないようにする。
                             # 探索済みの解にすぐ戻ってしまう (= 探索がループしてしまう) ことが少なくなることが期待される

        for i in range(iteration_num):
            best_change = float('inf') # その反復で最大の変化量を追跡する変数。無限大で初期化
            best_for_exchange_1, best_for_exchange_2 = -1, -1 # 最も改善が見込める交換を行う辺のインデックスを記録する変数
            current_length = self.calc_length_in_zone(tour)
            # 交換による経路長の変化量を計算。負の値なら改善している（短くなる）
            for a in range(n):
                if tour[a] in taboo_list:
                    continue
                for b in range(a+2, n): # 2番目の辺の開始都市のインデックスbは、a+2 から n-1 まで
                    if a == 0 and b == n - 1:  # a が最初の都市(0)で b が最後の都市(n-1)の場合はスキップ
                        continue
                    old_two_edges_distance = self.distance(tour[a], tour[(a+1) % n]) + self.distance( 
                        tour[b],tour[(b + 1) % n]
                    ) # a=nの時など、a+1のままだとIndexerrorになってしまう。経路は巡回しているので、a=nのときa+1=1
                    new_two_edges_distance = self.distance(tour[a], tour[b]) + self.distance(
                        tour[(a + 1) % n], tour[(b + 1) % n]
                    )
                    current_change = new_two_edges_distance - old_two_edges_distance
                    if current_change < best_change:  # 交換による経路長の変化量 < best_changeの場合bestを更新
                        best_change = current_change
                        best_for_exchange_1, best_for_exchange_2 = a, b

            taboo_list.append(tour[best_for_exchange_1])
            if len(taboo_list) > TravelingSalesman.max_length_taboo: #tabooリストのサイズが上限を超えた場合、最も古い要素を削除
                taboo_list.popleft()
            # 2-opt交換を実行。tour[a_best + 1] から tour[b_best] までの部分を反転させる
            tour[best_for_exchange_1 + 1 : best_for_exchange_2 + 1] = tour[best_for_exchange_2:best_for_exchange_1:-1]
            current_length += best_change
            if current_length < best_tour_length:
                best_tour_length = current_length
                best_tour = tour[:]
        return best_tour

    # 各ゾーンにおける最短の巡回路を計算し、それらを繋げゾーンを時計回りに訪問していく時の全体での最短順回路を求める
    def conbine_best_tours(self):
        zone_order = [(0,0),(1,0),(2,0),(2,1),(1,1),(0,1)] 
        all_tour = [] # 最終的な結合された経路 (ノードの元のインデックス)
        for r, c in zone_order: # ゾーンを時計回り順に訪問していく (0,0) -> (0,1) -> (0,2) -> (1,2) -> (1,1) -> (1,0)
            # print(f"r,c: {r,c}")
            index_list = self.divided_index_list[r][c]
            if not index_list: # このゾーンにノードがない場合はスキップ
                continue
            temporary_tour = self.solve_in_zone(index_list) # ゾーン内TSPの初期経路を最近傍法で計算
            best_tour = self.taboo_search_in_zone(temporary_tour) # 2-optとタブーサーチで経路を改善
            all_tour.extend(best_tour) # 計算した各ゾーンにおける最短経路を、全体の経路に追加する
            # 2-optとタブーサーチで最終経路を再度改善
            best_all_tour = self.taboo_search_in_zone(all_tour,iteration_num = 5) 
        return best_all_tour


    def main(self,input_file_path):
        self.address_list = read_input(input_file_path) # 入力ファイルから座標を読み込む
        for index,address in enumerate(self.address_list):
            self.address_dict[index] = address
        self.divide_city_in_zone() # 都市全体を2行3列の6ゾーンに分割する

        # 各ゾーンにおける最短の巡回路を計算し、それらを繋げゾーンを時計回りに訪問していく時の全体での最短順回路を求める
        final_best_tour = self.conbine_best_tours() 
        print_tour(final_best_tour) # 結果の経路を出力

if __name__ == '__main__': # ここに書くのはなるべく少なくする
    assert len(sys.argv) > 1 
    tsp = TravelingSalesman()
    tsp.main(sys.argv[1])
    