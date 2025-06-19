import sys
import collections
from collections import deque
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):
        # A mapping from a page ID (integer) to the page title.
        self.titles = {}
        # A mapping from a page title to the page ID (integer)
        self.ids = {}
        # A set of page links.
        self.dst_links = {} # src_id -> dst_id
        self.src_links = {} # dst_id -> src_id
        self.visited = set()

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.dst_links[id] = []
                self.src_links[id] = []
        print("Finished reading %s" % pages_file)

        self.ids = {title:id for id,title in self.titles.items()}

        # Read the links file into self.dst_links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.dst_links[src].append(dst)
                self.src_links[dst].append(src)
        print("Finished reading %s" % links_file)
        print()

    def find_farthest_node_from_src(self, start_id):
        distances_from_src = {} # ページIDごとの最短距離を格納
        route_from_src = {} # ページIDごとの最短距離を格納
        q = collections.deque()

        # 全てのノードの距離を無限大で初期化
        for page_id in self.titles:
            distances_from_src[page_id] = -1
            route_from_src[page_id] = set() # 各ノードの経路セットも初期化しておく

        # 開始ノードの距離を0とし、キューに追加
        distances_from_src[start_id] = 0
        q.append(start_id)

        # BFSを実行して各ノードの距離を計算
        while q:
            current_id = q.popleft()
            for neighbor_id in self.dst_links[current_id]:
                if not neighbor_id in self.visited:
                    if distances_from_src[neighbor_id] == -1:
                        distances_from_src[neighbor_id] = distances_from_src[current_id] + 1
                        route_from_src[neighbor_id] = route_from_src[current_id].copy()
                        route_from_src[neighbor_id].add(current_id)
                        q.append(neighbor_id)
        return distances_from_src,route_from_src

    # 既存のメソッド：特定の目標ノードへの最も遠いノードを見つける（逆方向のリンクを探索）
    def find_farthest_node_to_dst(self, goal_id):
        distances_to_dst = {} # ページIDごとの最短距離を格納
        route_to_dst = {}
        q = collections.deque()

        # 全てのノードの距離を無限大で初期化
        for page_id in self.titles:
            distances_to_dst[page_id] = -1
            route_to_dst[page_id] = set()

        # 目標ノードの距離を0とし、キューに追加
        distances_to_dst[goal_id] = 0
        q.append(goal_id)

        # 逆方向のリンク（src_links）を使ってBFSを実行し、各ノードの距離を計算
        while q:
            current_id = q.popleft()
            for neighbor_id in self.src_links[current_id]:
                if not neighbor_id in self.visited:
                    if distances_to_dst[neighbor_id] == -1:
                        distances_to_dst[neighbor_id] = distances_to_dst[current_id] + 1
                        route_to_dst[neighbor_id] = route_to_dst[current_id].copy()
                        route_to_dst[neighbor_id].add(current_id)
                        q.append(neighbor_id)
        return distances_to_dst,route_to_dst

    # 新しいメソッド：開始ノードからの距離と終了ノードへの距離の和が最大になるノードを見つける
    def find_node_with_max_total_distance(self, start_id, goal_id):
        # 1. 開始ノードからのすべてのノードへの距離を計算
        distances_from_src,route_from_src = self.find_farthest_node_from_src(start_id)
        # print(f"distances_from_src: {distances_from_src}, route_from_src: {route_from_src}") # debag

        # 2. 終了ノードへのすべてのノードからの距離を計算 (逆方向)
        distances_to_dst,route_to_dst = self.find_farthest_node_to_dst(goal_id)
        # print(f"distances_to_dst: {distances_to_dst}, route_to_dst: {route_to_dst}") # debag

        max_total_distance = -1
        node_with_max_total_distance = None

        # 3. すべてのノードを反復処理し、合計距離を計算して最大値を見つける
        for page_id in self.titles:
            dist_from_src = distances_from_src.get(page_id, 0)
            dist_to_dst = distances_to_dst.get(page_id, 0)
            set_from_src = route_from_src.get(page_id,())
            set_to_dst = route_to_dst.get(page_id,())

            # 到達不可能なノードはスキップ
            if dist_from_src <= 0 or dist_to_dst <= 0: # start,goalの場合,を排除
                continue
            if not set_from_src.isdisjoint(set_to_dst):
                continue

            current_total_distance = dist_from_src + dist_to_dst
            if current_total_distance > max_total_distance:
                max_total_distance = current_total_distance
                node_with_max_total_distance = page_id

        # 見つかったノードのIDと、その合計距離を返す
        return node_with_max_total_distance, max_total_distance

    def find_longer_path(self,start,goal):
        
        start_id = self.ids.get(start,-1) # Change from a title to the id <self.ids>
        assert start_id != -1, f"{start} is not found."
        goal_id = self.ids.get(goal,-1)
        assert goal_id != -1, f"{goal} is not found."
        
        longer_path = [start_id,goal_id]
        self.visited.add(start_id)
        self.visited.add(goal_id)

        i = 0
        while i <= len(longer_path)-2:
            via_id, distance = self.find_node_with_max_total_distance(longer_path[i], longer_path[i+1])
            print(f"via_title: {self.titles.get(via_id,None)}, distance: {distance},i: {i}") # Debag
            if via_id:
                longer_path.insert(i+1,via_id)
                self.visited.add(via_id)
            else:
                i += 1
            # print(f"longer_path: {longer_path}") # debag
        return longer_path

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)
    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    start_datetime = datetime.now()
    print("--- Debag list ---")
    longer_path = wikipedia.find_longer_path("渋谷","池袋")
    print("--- Result ---")
    print(f"the longer path from 渋谷 to 池袋:{longer_path}, the length is: {len(longer_path)}")
    end_datetime = datetime.now()
    elapsed_timedelta = end_datetime - start_datetime
    seconds = elapsed_timedelta.total_seconds()
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    print(f"the processing time is: {int(hours)}時間 {int(minutes)}分 {seconds:.2f}秒")