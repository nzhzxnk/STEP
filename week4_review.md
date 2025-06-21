### 逆dictの作成
* 外から入れるデータなので
* assertを入れて確認するべき
* len()が変化していないかで確認

### 経路を出す
* パスを一個求める chileに対するparentを保存しておく。
* パスを辿った時の長さを保存しておいて

## 案
* 現実的に有用　ランダムに求めて
* simlated aniring　焼きなまし　部分的に長い経路を入れ替える
* 訪問順序を考える
* Mikiさん　visitedで保存、直接パスを入れないような工夫
* ヒューリスティクス
* 訪問順序がいいと長い経路を見つけられる
* 訪問順序をランダムにして色々試す。
* スタックからpopしたときにvisited立てる 長い経路を見つけたい時、複数の経路を見つけたい時
* DFS がどんな経路を発見するかは訪問順序次第
* goalまでの距離で`links[node]`をソートする
* [これやってみろ](https://docs.google.com/presentation/d/1HYvWO5WVokc33SB_ccE2ONoN5MfyVCsZZ-2h29wyeBg/edit?slide=id.g3606954bc18_0_61#slide=id.g3606954bc18_0_61)
* やっぱりDFSを使うのがいいかな
* 私のやつをやや諦めるには[これ](https://docs.google.com/presentation/d/1HYvWO5WVokc33SB_ccE2ONoN5MfyVCsZZ-2h29wyeBg/edit?slide=id.g3606954bc18_0_82#slide=id.g3606954bc18_0_82)をランダムにする

* 最長経路
* dijkstra
* Remanfond,WorshdFkoid
* 終るように何かを諦める
P 問題　-> 答え 多項式時間で解ける
NP 答え -> 問題 多項式時間で検証できる
NP問題の多くはあるNP問題に帰着できる場合が多い
NP complete = desision problem
NP hard (NP困難) = function probrem
NP 答えみても問題をも対しているか検証することすら難しい
「ある問題 L が多項式時間で解けるならば、別の問題 H も多項式時間で解ける」とき、「L は H よりも難しい」という
L=オムライス, H=オムレツ
[要復習](https://docs.google.com/presentation/d/1l2NbSImuppETfdOdYCJlVP5wDjmAHR-IF61H1ahs3QY/edit?slide=id.g24ea1e949fa_0_327#slide=id.g24ea1e949fa_0_327)

ヒューリスティクス(Heuristics)近似買い

私の関数って計算量いくつ？


浮動小数点
128,64,32,16bit
IEE754
2**e
rangeがきまってる
float

読みやすい綺麗なコード


貪欲法(Greedy Algorithm)
2.5 opt、3 opt
焼きなまし法
遺伝的アルゴリズム
蟻コロニー最適化
他にもいろいろ
