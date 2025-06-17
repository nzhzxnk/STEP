# Week4 Homework Summary
## 各レポジトリの構成
```mermaid
graph BT
    subgraph Week 4 Challenge Quiz
    W4H4[Challenge Quiz]
    W4H4 --> W4H4D[dfs_1.py]
    end

    subgraph Week 4 Homework 3
    W4H3[week4_homework_3]
    W4H3 --> W4H3W[wikipedia_3.py]
    end

    subgraph Week 4 Homework 2
    W4H2[week4_homework_2]
    W4H2 --> W4H2W[wikipedia_2.py]
    end

    subgraph Week 4 Homework 1
    W4H1[week4_homework_1]
    W4H1 --> W4H1W[wikipedia_1.py]
    end

    subgraph Week 4 General
    W4G[week4_general]
    W4G --> W4GH[week4_homework_summary.md]
    W4G --> W4GC[week4_classmemo.md]
    end
```

---
## Homework1

### 内容
* [データセットのフォーマット](https://docs.google.com/presentation/d/1m6uTcNhnmjky578GVXMbyOCu2-yM4lNqU8FR5eJdx_I/edit?slide=id.g1e13c1d4e24_1_507#slide=id.g1e13c1d4e24_1_507)
* あるページから別のページへの最短経路を出力する。
* find_shortest_path()関数を作成する。
* BFSを利用する。

### 提出コード
[wikipedia_1.py](https://github.com/nzhzxnk/STEP/blob/main/week4_homework_1/wikipedia_1.py)

### 説明
1. `def __init__(self, pages_file, links_file):`

* `self.titles`, `self.ids`, `self.links` という3つのdictionaryを作成。
* `self.titles`: pages_small/medium/large.txtファイルを読み込み、`{ id_1:title_1, id_2:title_2, ...}`という形で保存。
* `self.ids`: pages_small/medium/large.txtファイルを読み込み、`{ title_1:id_1, title_2:id_2, ...}`という形で保存。
* `self.links`: links_small/medium/large.txtファイルを読み込み、`{ id_1:[dst_id_1, dst_id_2], id_2:[], ...}`という形で保存。子リンクがないsource_idに対しても空リストを持っている。

2. `def find_shortest_path(self, start, goal):`

* start, goalはタイトル名で与えられるので、`self.ids`を用いてstart_id, goal_idに変換する。
* getメゾットを用いて、`self.ids`に与えられたタイトル名が含まれなければ`-1`を返す。
* さらに`assert start_id != -1, f"{start} is not found."`によって、与えられたタイトル名がデータセットになかった場合には`Assertion Error`となる。

* `visited`: すでに訪れたページのidを`(id_1, id_2, ...)`というsetの形で保存しておく。このコードではqueueに追加した際に、visitedにもidを追加する仕組みとした。
* `q`: 探索する予定のページのidとそのページに至るまでの経路リストを`[(id_1, [id_2, id_3, id_4]), (id_5, [id_6, id_7]), ...] `というdequeの形で保存しておく。appendで右側から追加、popleftで左側から取り出しすることで順序性を保つ仕組みとなっている。
* `shortest_routes`: 最短経路の候補を格納しておくリスト。`[[title_1, title_2, ...], [title_3, title_4, ...], ...]`という多重リストの形で保存しておく。
* `min_route_length`: 現在の最短経路の長さを保存しておく。これ以上長い経路は以降探索しないようにすることで、無駄な経路探索を減少させた。

* `q`からpopleftした要素を、`is_visiting_id`(int), `route_taken`(list) とする。
* `route_taken`がすでに`min_route_length`以上の経路は、それ以降探索しない。
* `is_visiting_id`からリンクされている`dst_id`の中で、`visited`に含まれていないものがあれば、そこに進んで経路探索する。
* `dst_id == goal_id`であった場合は、`len(new_route)`と`min_route_length`の条件によって実行が異なる。
* `len(new_route) > min_route_length`の場合は、その経路は最短経路でないので何もしない。
* `len(new_route) == min_route_length`の場合は、その経路は最短経路候補なので`shortest_routes`に追加する。
* `len(new_route) < min_route_length`の場合は、その経路は最短経路候補だが今までの`shortest_routes`は最短経路ではなくなる。`shortest_routes`と`min_route_length`を更新する。
* `shortest_routes`に追加する際には`shortest_routes = [[self.titles[id] for id in new_route]] `とし、idではなくtitleのリストとして追加する。
* `dst_id != goal_id`であった場合は、今後も経路探索を続ける必要があるため`q`に追加する。
* `start_id == goal_id`のような例外的な場合については別途対処する。

### 入力と出力結果
1. medium set, `wikipedia.find_shortest_path("渋谷", "小野妹子")`

the shortest path is: 渋谷 -> ギャルサー_(テレビドラマ) -> 小野妹子

2. large set, `wikipedia.find_shortest_path("渋谷", "小野妹子")`

the shortest path is: 渋谷 -> ギャルサー_(テレビドラマ) -> 小野妹子

3. medium set, `wikipedia.find_shortest_path("流体力学", "蒙古タンメン")`

the shortest path was not found.

4. large set, `wikipedia.find_shortest_path("流体力学", "蒙古タンメン")`

the shortest path is: 流体力学 -> 1653年 -> 6月23日 -> ななもり。 -> 蒙古タンメン

5. medium set, `wikipedia.find_shortest_path("文脈自由文法", "ユニクロ")`

the shortest path is: 文脈自由文法 -> 形式言語 -> 言語 -> 広辞苑 -> ユニクロ

the shortest path is: 文脈自由文法 -> 形式言語 -> 英語 -> Q -> ユニクロ

the shortest path is: 文脈自由文法 -> 形式言語 -> ISBN -> 流通 -> ユニクロ

the shortest path is: 文脈自由文法 -> 形式言語 -> プロパガンダ -> カイザー・ヴィルヘルム記念教会 -> ユニクロ

the shortest path is: 文脈自由文法 -> 形式言語 -> 修辞学 -> 早稲田大学 -> ユニクロ

the shortest path is: 文脈自由文法 -> プログラミング言語 -> 日本語 -> 日本の経済 -> ユニクロ

the shortest path is: 文脈自由文法 -> プログラミング言語 -> 日本語 -> 日本の百貨店 -> ユニクロ

the shortest path is: 文脈自由文法 -> プログラミング言語 -> 1980年代 -> キース・ヘリング -> ユニクロ

the shortest path is: 文脈自由文法 -> プログラミング言語 -> Ruby -> 松江市 -> ユニクロ

the shortest path is: 文脈自由文法 -> プログラミング言語 -> 1950年代 -> カンボジア -> ユニクロ

the shortest path is: 文脈自由文法 -> プログラミング言語 -> 人間 -> 養老孟司 -> ユニクロ

the shortest path is: 文脈自由文法 -> プログラミング言語 -> ユビキタスコンピューティング -> RFID -> ユニクロ

the shortest path is: 文脈自由文法 -> プログラミング言語 -> 電子投票 -> 広島県 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> 1988年 -> 6月19日 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> 1988年 -> 内田篤人 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> 2001年 -> 新宿区 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> 1996年 -> トムス・エンタテインメント -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> 1996年 -> 三吉彩花 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> 1999年 -> ジョジョの奇妙な冒険 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> 1999年 -> 吉良吉影 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> 国際連合 -> グラミン銀行 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> 1928年 -> 平良とみ -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> 1928年 -> しんぶん赤旗 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> 政治 -> 障害者 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> ソビエト連邦 -> ジーンズ -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> アメリカ同時多発テロ事件 -> 日経平均株価 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> 大学院 -> 帝京平成大学 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> 12月7日 -> 宮本笑里 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> マサチューセッツ工科大学 -> キリンホールディングス -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> 講談社 -> セミヌード -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> マスメディア -> 姫路駅 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> ベトナム戦争 -> 水木しげる -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> 労働者 -> 非正規雇用 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> 労働者 -> 変形労働時間制 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> ジェレミ・ベンサム -> 毛皮 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> 鶴見俊輔 -> 福島瑞穂 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> カリフォルニア大学バークレー校 -> 竹内弘高 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> カリフォルニア大学バークレー校 -> 明治大学 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> コロンビア大学 -> 松任谷由実 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> 文藝春秋 -> 週刊文春 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> みすず書房 -> 池田香代子 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> ニューヨーク -> 多国籍企業 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> 研究社 -> 吉祥寺 -> ユニクロ

the shortest path is: 文脈自由文法 -> ノーム・チョムスキー -> いいだもも -> 水戸市 -> ユニクロ

the shortest path is: 文脈自由文法 -> 生成文法 -> 1965年 -> リポビタンD -> ユニクロ

the shortest path is: 文脈自由文法 -> 生成文法 -> 1965年 -> 小林靖子 -> ユニクロ

the shortest path is: 文脈自由文法 -> 生成文法 -> 1965年 -> 野村万蔵_(9世) -> ユニクロ

the shortest path is: 文脈自由文法 -> アルゴリズム -> 著作権 -> 多摩市 -> ユニクロ

the shortest path is: 文脈自由文法 -> アルゴリズム -> ハッシュ関数 -> スーパーマーケット -> ユニクロ

the shortest path is: 文脈自由文法 -> ALGOL -> 1958年 -> 日本コカ・コーラ -> ユニクロ

the shortest path is: 文脈自由文法 -> ALGOL -> 1958年 -> 桃屋 -> ユニクロ

the shortest path is: 文脈自由文法 -> ALGOL -> 9月1日 -> 八王子市 -> ユニクロ

the shortest path is: 文脈自由文法 -> ALGOL -> 9月1日 -> 羽生市 -> ユニクロ

the shortest path is: 文脈自由文法 -> ALGOL -> ケース・ウェスタン・リザーブ大学 -> ファーストリテイリング -> ユニクロ

the shortest path is: 文脈自由文法 -> ALGOL -> ケース・ウェスタン・リザーブ大学 -> ロッテホールディングス -> ユニクロ

the shortest path is: 文脈自由文法 -> パーニニ -> ヒンドゥー教 -> 禅宗 -> ユニクロ

the shortest path is: 文脈自由文法 -> パーニニ -> ダルマ -> 小田原市 -> ユニクロ

the shortest path is: 文脈自由文法 -> タミル語 -> 大野晋 -> 江東区 -> ユニクロ

the shortest path is: 文脈自由文法 -> タミル語 -> チェンナイ -> 現代自動車 -> ユニクロ

the shortest path is: 文脈自由文法 -> タミル語 -> 都市伝説 -> ロッテリア -> ユニクロ

the shortest path is: 文脈自由文法 -> バッカス・ナウア記法 -> 1959年 -> 田口ランディ -> ユニクロ

the shortest path is: 文脈自由文法 -> バッカス・ナウア記法 -> 姓 -> 山口県 -> ユニクロ

the shortest path is: 文脈自由文法 -> バッカス・ナウア記法 -> 姓 -> 小平市 -> ユニクロ

the shortest path is: 文脈自由文法 -> タプル -> 数詞 -> 渋谷 -> ユニクロ

the shortest path is: 文脈自由文法 -> 理論計算機科学 -> 1931年 -> 津田沼 -> ユニクロ

the shortest path is: 文脈自由文法 -> 理論計算機科学 -> 1948年 -> ロッテ -> ユニクロ

the shortest path is: 文脈自由文法 -> 理論計算機科学 -> 1948年 -> 糸井重里 -> ユニクロ

the shortest path is: 文脈自由文法 -> 理論計算機科学 -> 1948年 -> 重光武雄 -> ユニクロ

the shortest path is: 文脈自由文法 -> スイスドイツ語 -> スイス -> ロジャー・フェデラー -> ユニクロ

the shortest path is: 文脈自由文法 -> 畳語 -> 愛称 -> サッカー日本女子代表 -> ユニクロ

### 修正前コードの検討

* このコードに修正する前に書いたコードがあったが、これだと実行時間が非常に長すぎて使い物にならなかった。
* 無限ループなど機能的に誤りがあったのか、単に無駄な探索が多すぎたのか、少し検討したい

```python3 []
 while q:
            count += 1
            # print(count) #debag
            is_visiting_id, route_taken = q.popleft()
            visited.add(is_visiting_id) # Add is_visiting_id to visited.
            if not find_goal:
                if is_visiting_id == goal_id: # If reach the goal, return route taken.
                    find_goal = True
                    path = [self.titles[id] for id in route_taken]
                    shortest_path_length = len(path)
                    shortest_paths.append(path) # Change from a id to the title. <self.titles>
                else:
                    for dst_id in self.links[is_visiting_id]:  # Search for destinations of is_visiting_id.
                        if dst_id in visited: # Check for multiple visits. <visited>
                            continue
                        else: # If the destination was NOT visited, append dst_id,route_taken to queue. 
                            q.append((dst_id,route_taken+[dst_id])) # add dst_id to route_taken 
            else:
                if is_visiting_id == goal_id: # If reach the goal, return route taken.
                    if len([self.titles[id] for id in route_taken]) <= shortest_path_length:
                        shortest_paths.append([self.titles[id] for id in route_taken]) # Change from a id to the title. <self.titles>
        return shortest_paths
```
---
## Homework2

### 内容
* ページランクを計算して重要度の高いページトップ10を出力する。
* ind_most_popular_pages() 関数を作成する。
* 時間計算量はO(N+E)。
* 正しさの確認方法: ページランクの分配と更新を何回繰り返しても、全ノードのページランクの合計値が一定に保たれることを確認
* 収束条件: ページランクの更新が完全に収束するのは時間がかかりすぎるので、更新が十分少なくなったら止める。例）∑(new_pagerank[i] - old_pagerank[i])^2 < 0.01

### 提出コード
[wikipedia_2.py](https://github.com/nzhzxnk/STEP/blob/main/week4_homework_2/wikipedia_2.py)

### 説明

* `old_pagerank`: 新たな計算開始前のページidとpagerankを、`{id_1:1.0, id_2:1.0, ...}`という形で保存しておく。
* `converging`: pagerankの計算が収束していれば`True`、していなければ`False`とする。`converging == False`であれば計算を続ける。
* `num_pages`: 全体のページ数。また、pagerankの合計は常にこれと同じになる。

* `new_pagerank`: 新たな計算後のページidとpagerankを、`{id_1:1.0, id_2:1.0, ...}`という形で保存しておく。はじめは全て`0.0`に初期化しておく。
* `random_jump_value`: すべてのページに均等に振り分けられる分のpagerankの合計。
* `torerance`: 計算前後で生じた差の合計。各ページについての`(new_pagerank[id]-old_pagerank[id])**2 `の合計で表す。

* `self.links.items()`の各要素を`src_id`(親ページのid),`dst_ids`(子ページのidのlist)とする。
* `src_id`からリンクされた子ページがない場合、`old_pagerank[src_id]` を全て`random_jump_value`に加える。
* `src_id`からリンクされた子ページがある場合、`old_pagerank[src_id]*0.85`を子ページに均等に振り分ける。また`old_pagerank[src_id]*0.15`を`random_jump_value`に加える。
* 計算の最後に、`random_jump_page`をすべてのページに均等に振り分ける。
* `assert abs(sum(new_pagerank.values()) - num_pages) < 1e-4, f"the pagerank system is wrong.{sum(new_pagerank.values()) - num_pages} "`で、pagerankの合計が`num_pages`と等しくない場合はAssertion Errorを起こすようにした。
* mediumのデータセットで`AssertionError: the pagerank system is wrong.-1.0110670700669289e-06`というerrorが出たので、`1e-4`程度が妥当な基準と考えた。
* 浮動小数点や除算を含む計算であり、完全に一致するわけではないので、`sum(new_pagerank.values()) == num_pages`は用いなかった。
* `torerance < 0.01`となったら、`converging = True`として計算のループを抜ける。
* `top10_pagerank_ids`: 計算が終了したら`new_pagerank.items()`をpagerankに着目し降順に並べ、上から順に10番目までを切り出してリストにする。

### 出力結果
1. small set

the most important 10 pages are: 
C
D
B
E
F
A

2. medium set

the most important 10 pages are: 
英語
ISBN
2006年
2005年
2007年
東京都
昭和
2004年
2003年
2000年

3. large set
the most important 10 pages are: 
英語
日本
VIAF_(識別子)
バーチャル国際典拠ファイル
アメリカ合衆国
ISBN
ISNI_(識別子)
国際標準名称識別子
地理座標系
SUDOC_(識別子)


---
## Homework3

### 内容
* Wikipedia のグラフについて「渋谷」から「池袋」まで、同じページを重複して通らない、できるだけ長い経路を発見してください！！

### 提出コード

### 説明

---
## Challenge Quiz

### 内容
*　再帰版 DFS と同じたどり方をする DFS をスタックを使って書く。
* "A -> B -> C -> D -> E -> F" が最初に発見される DFS をスタックで書けたら合格
* 解法は何種類かある
* [参考スライド](https://docs.google.com/presentation/d/1m6uTcNhnmjky578GVXMbyOCu2-yM4lNqU8FR5eJdx_I/edit?slide=id.g230e6d63cfe_0_443#slide=id.g230e6d63cfe_0_443)

### 提出コード
[dfs_comparison.py](https://github.com/nzhzxnk/STEP/blob/main/week4_homework_4/dfs_comparison.py)

### 説明
1. `def dfs_with_stack_in_the_recursion_order`
* 

---
## DFSの比較
まだ作成中
[DFS Comparison](https://docs.google.com/presentation/d/1FUJFe_oBdW1lrlUxmAVQO3OYFPJC0O_AsZbbhZ1TGa0/edit?usp=sharing)
