## Homework
---
### 内容(week5と同様)
* 巡回セールスマン問題 (Travelling Salesperson Problem, TSP) を解決するアルゴリズムを設計
* 都市のリストと、各都市間の距離が与えられたとき、各都市をちょうど一度ずつ訪問し、出発地に戻る最短経路は何か？
---
### データフォーマット
#### 各ファイルの説明
| Challenge   | N (= the number of cities) | input file   | output taboo | output divide|
| :---------- | :------------------------- | :----------- | :----------- | :----------- |
| Challenge 0 | 5                          | input_0.csv  | taboo_0.csv  | divide_6.csv |
| Challenge 1 | 8                          | input_1.csv  | taboo_1.csv  | divide_6.csv |
| Challenge 2 | 16                         | input_2.csv  | taboo_2.csv  | divide_6.csv |
| Challenge 3 | 64                         | input_3.csv  | taboo_3.csv  | divide_6.csv |
| Challenge 4 | 128                        | input_4.csv  | taboo_4.csv  | divide_6.csv |
| Challenge 5 | 512                        | input_5.csv  | taboo_5.csv  | divide_6.csv |
| Challenge 6 | 2048                       | input_6.csv  | taboo_6.csv  | divide_6.csv |
| Challenge 7 | 8192                       | input_7.csv  | taboo_7.csv  | divide_7.csv |
詳しくは[week5_homework_summary](https://github.com/nzhzxnk/STEP/blob/main/week5_general/week5_homework_summary.md)を参照

---
### 方針
* Nの規模がかなり大きくなるので、ゾーンを分けて考える階層的TSPを実装する。
* week5のコードの出力経路をvisualizerで確認したところ、基本は外周を一周まわる経路が元になっており、ところどころ内側に入り込むようにして都市を訪問している形であることが観察できた。
* この経路が最適な巡回方法であると仮定すると、ゾーンを2行3列に分割し一周まわる経路を基準とし、ゾーン内での最短巡回経路を求め繋げる方法によってより最適な解を求めることができるのではないかと考えた。

---
### 今後やりたいこと
* 他の方のコードを参考にして考えたい。
* Nの規模に応じて、最適なヒューリスティクスを考えたい。
    * 2.5, 3-opt法　理解はしたしできそう
    * 焼きなまし法 (Simulated Annealing)　できるかも？
    * 一つ一つのNが小さくなれば。動的計画法 (DP)もあり？最適解を確実に出せるから
    * 遺伝的アルゴリズム　？
    * MSTベースの近似アルゴリズム　？
* ゾーン分割の方法や、ゾーン内の都市の数をどのくらいに調整するか
* ゾーン内で開始点。終了点を固定して、巡回TSPではなくパスTSPとしてといた方が最適化されそうと考えたが方法がわからない

---
### 提出コード
* [solver_divide](https://github.com/nzhzxnk/STEP/blob/main/week6_homework/solver_divide.py)　
* 基本のTSPは、最近傍法 (Nearest Neighbor)を使って暫定経路を求め、禁断探索法、2opt法を何度か反復して行い経路を修正する方針とした。
* ゾーンを2行3列に分割し一周まわる経路を基準とし、ゾーン内での最短巡回経路を求め繋げる方法を実装した。
* クラス変数インスタンス変数を使い分けて実装した
---
### 結果
* iteration_num=500、max_length_taboo=20で試していきたい

---
### 考察（計算量など）

