import sys
from wikipedia_3 import Wikipedia # wikipedia_converter.py から Wikipedia クラスをインポート

def run_converter_app(pages_file, links_file):
    try:
        # Wikipedia クラスのインスタンスを作成し、データをロード
        print("Wikipediaデータをロード中...")
        wiki_data = Wikipedia(pages_file, links_file)
        print("データのロードが完了しました。")
        print("\n--- 変換 ---")
        print("1. タイトルからIDへ変換")
        print("2. IDからタイトルへ変換")
        print("q. 終了")

        while True:
            choice = input("選択してください (1/2/q): ").strip().lower()

            if choice == '1':
                title = input("変換したいタイトルを入力してください: ").strip()
                if title in wiki_data.ids:
                    page_id = wiki_data.ids[title]
                    print(f"タイトル '{title}' のIDは '{page_id}' です。")
                else:
                    print(f"エラー: タイトル '{title}' は見つかりませんでした。")
            elif choice == '2':
                id_str = input("変換したいIDを入力してください: ").strip()
                try:
                    page_id = int(id_str)
                    if page_id in wiki_data.titles:
                        title = wiki_data.titles[page_id]
                        print(f"ID '{page_id}' のタイトルは '{title}' です。")
                    else:
                        print(f"エラー: ID '{page_id}' は見つかりませんでした。")
                except ValueError:
                    print("エラー: 無効なIDです。整数を入力してください。")
            elif choice == 'q':
                print("終了")
                break
            else:
                print("無効な選択です。'1', '2', または 'q' を入力してください。")

    except FileNotFoundError as e:
        print(f"エラー: 必要なデータファイルが見つかりません。パスを確認してください: {e}")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")

if __name__ == "__main__":
    # ここで pages.txt と links.txt のパスを指定します。
    # converter_app.py と同じディレクトリにある場合:
    default_pages_file = "/Users/hayashiayano/Desktop/STEP/wikipedia_dataset/pages_large.txt"
    default_links_file = "/Users/hayashiayano/Desktop/STEP/wikipedia_dataset/links_large.txt"

    # もしコマンドライン引数でファイルパスを指定したい場合
    if len(sys.argv) == 3:
        pages_file = sys.argv[1]
        links_file = sys.argv[2]
    else:
        pages_file = default_pages_file
        links_file = default_links_file
        print(f"使用法: python {sys.argv[0]} [pages_file] [links_file]")
        print(f"デフォルトファイルを使用します: {default_pages_file}, {default_links_file}")

    run_converter_app(pages_file, links_file)





        # 新しいメソッド：特定の開始ノードから最も遠いノードを見つける
    def find_farthest_node_from(self, start_title):
        start_id = self.ids.get(start_title, -1)
        if start_id == -1:
            print(f"エラー: 開始ノード '{start_title}' がグラフに存在しません。")
            return None, 0 # (Farthest Node Title, Distance)

        distances = {} # ページIDごとの最短距離を格納
        queue = collections.deque()

        # 全てのノードの距離を無限大で初期化
        for page_id in self.titles: # self.titlesのキーは全てのページIDを含む
            distances[page_id] = float('inf')

        # 開始ノードの距離を0とし、キューに追加
        distances[start_id] = 0
        queue.append(start_id)

        farthest_id = start_id
        max_distance = 0

        while queue:
            current_id = queue.popleft()

            # 現在のノードがこれまでの最遠ノードより遠ければ更新
            if distances[current_id] > max_distance:
                max_distance = distances[current_id]
                farthest_id = current_id

            # 隣接ノードを探索
            for neighbor_id in self.links[current_id]:
                # まだ訪れていない（距離が無限大の）ノードの場合
                if distances[neighbor_id] == float('inf'):
                    distances[neighbor_id] = distances[current_id] + 1
                    queue.append(neighbor_id)
        
        # 最終的な最も遠いノードのタイトルを返す
        return farthest_id, max_distance

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)
    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # # Homework #1a
    # paths = wikipedia.find_longer_path("渋谷", "池袋")
    # if paths:
    #     for path in paths:
    #         print(f"the longer path is: {" -> ".join(path)}")
    # else:
    #     print("the longer path was not found.")
    print("\n--- 最も遠いページ ---")
    farthest_page_id, distance_to_farthest = wikipedia.find_farthest_node_from("2006年の映画/1月")
    if farthest_page_id:
        print(f"最も遠いページ: {farthest_page_id}, 距離: {distance_to_farthest}")
    else:
        print(f"到達可能なページが見つかりませんでした。")
    # 渋谷から最も遠いページ: 375029, 距離: 13


    最短経路でもいいから