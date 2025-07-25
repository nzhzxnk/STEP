## Homework
---
### 内容
* 巡回セールスマン問題 (Travelling Salesperson Problem, TSP) を解決するアルゴリズムを設計
* 都市のリストと、各都市間の距離が与えられたとき、各都市をちょうど一度ずつ訪問し、出発地に戻る最短経路は何か？
* 各出力ファイル output_{0-6}.csv をプログラムの出力で上書きする。
* 出力の経路長をスコアボードに入力。もちろん経路は短いほど良い。
---
### データフォーマット
#### 各ファイルの説明
| Challenge   | N (= the number of cities) | Input file   | Output file  |
| :---------- | :------------------------- | :----------- | :----------- |
| Challenge 0 | 5                          | input_0.csv  | output_0.csv |
| Challenge 1 | 8                          | input_1.csv  | output_1.csv |
| Challenge 2 | 16                         | input_2.csv  | output_2.csv |
| Challenge 3 | 64                         | input_3.csv  | output_3.csv |
| Challenge 4 | 128                        | input_4.csv  | output_4.csv |
| Challenge 5 | 512                        | input_5.csv  | output_5.csv |
| Challenge 6 | 2048                       | input_6.csv  | output_6.csv |
* solver_random.py -  最も基本的なサンプル？
* solver_greedy.py - 貪欲アルゴリズムを使用したサンプル
* sample/random_{0-6}.csv - solver_random.py によるサンプル出力ファイル
* sample/greedy_{0-6}.csv - solver_greedy.py によるサンプル出力ファイル
* sample/sa_{0-6}.csv - 謎のサンプル出力ファイル？solverは与えられていない
* output_{0-6}.csv - プログラムの出力で上書きする
* output_verifier.py - 出力ファイルを検証し、経路長を出力する
* input_generator.py - 入力ファイル input_{0-6}.csv を作成するために使用されたスクリプト
* visualizer/ - ビジュアライザーのディレクトリ

#### 入力フォーマット
* 入力はN + 1 行。
* 最初の行は常に`x,y`、それに続いて N 行があり、各行は i 番目の都市の場所、つまり `xi,yi` (`xi`, `yi` は浮動小数点数) を表す。
```python3[]
x,y
x_0,y_0
x_1,y_1
...
x_N-1,y_N-1
```
#### 出力フォーマット
* 出力は N + 1 行。
* 最初の行は "index"、それに続いて N 行があり、各行は都市のインデックスであり、訪問順序を表す。
```python3[]
index
v_0
v_1
v_1
...
v_N-1
```
---
### 方針
* Nの規模に応じて、最適なヒューリスティクスを考えたい。

#### Nが小さい場合 (N=5, 8, 16)
* 動的計画法 (DP): 最適解を確実に出せる？

#### Nが中〜大規模の場合 (N=64, 128, 512, 2048)
**ある程度の経路の作成**
* 最近傍法 (Nearest Neighbor)　solver_greedy.pyとやってること一緒だった、、
* MSTベースの近似アルゴリズム

**経路の改善（局所探索）**
* 2-opt法: 交差した部分を取り除くのを繰り返す。

**大域的な最適化（メタヒューリスティクス）**
* 焼きなまし法 (Simulated Annealing)
* 禁断探索法 (Taboo Search): 探索済みの解にすぐ戻ってしまう (= 探索がループしてしまう) ことが少なくなることが期待される
---
### 提出コード
* [solver_taboo](https://github.com/nzhzxnk/STEP/blob/main/week5_homework/solver_taboo.py)　
* [output_generator](https://github.com/nzhzxnk/STEP/blob/main/week5_homework/output_generator.py)
* 貪欲法の一つである最近傍法 (Nearest Neighbor)を使って暫定の経路を求めた。
* 禁断探索法、2opt法を何度か反復して行い、経路を修正した。
---
### 説明
* 解を適当に作り、暫定解 X とする。最良解 B を X で初期化する。禁断リストを空で初期化する。禁断リストのサイズの上限を決める
* 一定の回数、以下を繰り返す
* 暫定解 X を少しだけ変更したもの (X の近傍) であって、なおかつ禁断リストに含まれていない解のうち最も良い解 X' を求め、X を X' で更新する。X が B より真に良い場合は、B を X で更新する。解 X を禁断リストの先頭に加える。禁断リストのサイズが上限を超えた場合は禁断リストに含まれている最も古い解を削除する
* 最良解 B を解として出力する
* 巡回路 X に含まれる 2 本の辺を繋ぎ変えたものを X の近傍とする
* 禁断リストには繋ぎ変えた辺の端点のうち巡回路 X の先頭に最も近い都市 t を入れる。つまり、t を端点として持つ辺を繋ぎ変えて解を更新した後しばらくは（禁断リストにいる間は）、t を端点として持つ辺は繋ぎ変えない
---
### 結果
* iteration_numは改善を行う回数、max_length_tabooはタブーリストの大きさ

* iteration_num = 150, max_length_taboo = 10
| Challenge   | output      | sample/random   | sample/greedy   | sample/sa       |
| :---------- | :---------- | :-------------- | :-------------- | :-------------- |
| Challenge 0 | 3291.62     | 3862.20         | 3418.10         | 3291.62         |
| Challenge 1 | 3832.29     | 6101.57         | 3832.29         | 3778.72         |
| Challenge 2 | 4670.27     | 13479.25        | 5449.44         | 4494.42         |
| Challenge 3 | 8629.41     | 47521.08        | 10519.16        | 8150.91         |
| Challenge 4 | 11061.89    | 92719.14        | 12684.06        | 10675.29        |
| Challenge 5 | 20880.95    | 347392.97       | 25331.84        | 21119.55        |
| Challenge 6 | 42516.96    | 1374393.14      | 49892.05        | 44393.89  

* iteration_num = 300, max_length_taboo = 20
| Challenge   | output      | sample/random   | sample/greedy   | sample/sa       |
| :---------- | :---------- | :-------------- | :-------------- | :-------------- |
| Challenge 0 | 3291.62     | 3862.20         | 3418.10         | 3291.62         |
| Challenge 1 | 3832.29     | 6101.57         | 3832.29         | 3778.72         |
| Challenge 2 | 4750.00     | 13479.25        | 5449.44         | 4494.42         |
| Challenge 3 | 8381.67     | 47521.08        | 10519.16        | 8150.91         |
| Challenge 4 | 10964.05    | 92719.14        | 12684.06        | 10675.29        |
| Challenge 5 | 20952.14    | 347392.97       | 25331.84        | 21119.55        |
| Challenge 6 | 41492.06    | 1374393.14      | 49892.05        | 44393.89 

* iteration_num = 500, max_length_taboo = 50
| Challenge   | output      | sample/random   | sample/greedy   | sample/sa       |
| :---------- | :---------- | :-------------- | :-------------- | :-------------- |
| Challenge 0 | 3291.62     | 3862.20         | 3418.10         | 3291.62         |
| Challenge 1 | 3832.29     | 6101.57         | 3832.29         | 3778.72         |
| Challenge 2 | 4750.00     | 13479.25        | 5449.44         | 4494.42         |
| Challenge 3 | 8700.40     | 47521.08        | 10519.16        | 8150.91         |
| Challenge 4 | 11114.79    | 92719.14        | 12684.06        | 10675.29        |
| Challenge 5 | 20978.97    | 347392.97       | 25331.84        | 21119.55        |
| Challenge 6 | 41347.30    | 1374393.14      | 49892.05        | 44393.89        |

* iteration_num = 500, max_length_taboo = 10
| Challenge   | output      | sample/random   | sample/greedy   | sample/sa       |
| :---------- | :---------- | :-------------- | :-------------- | :-------------- |
| Challenge 0 | 3291.62     | 3862.20         | 3418.10         | 3291.62         |
| Challenge 1 | 3832.29     | 6101.57         | 3832.29         | 3778.72         |
| Challenge 2 | 4656.80     | 13479.25        | 5449.44         | 4494.42         |
| Challenge 3 | 8629.41     | 47521.08        | 10519.16        | 8150.91         |
| Challenge 4 | 11061.89    | 92719.14        | 12684.06        | 10675.29        |
| Challenge 5 | 20880.65    | 347392.97       | 25331.84        | 21119.55        |
| Challenge 6 | 41441.94    | 1374393.14      | 49892.05        | 44393.89        |

* iteration_num = 750, max_length_taboo = 20
| Challenge   | output      | sample/random   | sample/greedy   | sample/sa       |
| :---------- | :---------- | :-------------- | :-------------- | :-------------- |
| Challenge 0 | 3291.62     | 3862.20         | 3418.10         | 3291.62         |
| Challenge 1 | 3832.29     | 6101.57         | 3832.29         | 3778.72         |
| Challenge 2 | 4750.00     | 13479.25        | 5449.44         | 4494.42         |
| Challenge 3 | 8381.67     | 47521.08        | 10519.16        | 8150.91         |
| Challenge 4 | 10935.95    | 92719.14        | 12684.06        | 10675.29        |
| Challenge 5 | 20952.14    | 347392.97       | 25331.84        | 21119.55         |
| Challenge 6 | 41425.14    | 1374393.14      | 49892.05        | 44393.89        |
* iteration_num = 1000, max_length_taboo = 20でも結果変わらず。

* これらの数をできるだけ増やしていけば精度上がる、というわけでもなかった。
* max_length_taboo = 20くらいの時がいいのか

---
### 考察（計算量など）
これからかきます
