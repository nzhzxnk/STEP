## [コードの反省点]()

### 質問したいこと
* 計算量の見積もりについて
* anagram1_1,anagram1_2のそれぞれの計算量が合っているのか？
* そもそもやろうとしてることあってるよね？
* より良いコードの評価基準がなんなのか？基準がわからなくて直すにも直せないどう勉強したらいいのか
* 時間的計算量実行時間、空間的計算量メモリ、関数やファイルはどのように分割するべき？、具体的にコードのどこを修正するべきか
* テストケースとかででてきたself.(def_name) selfをなぜ明示するのかわからない
* counterとかbisectとか標準のモジュールは利用していい？というか使い方練習した方がいい？
* 入力を正規化する方法とかもたくさんあるのかな

###これからやりたいこと
* 私のコードではang_dictを共通して使っていたんだけど、計算量を少なくするために他のファイルで作ったang_dictを使いまわしたい
* angram2でdictが増えて煩雑になってしまった気がする。
* sort_word <-> word, sort_word <-> score, sort_word <-> counterではなく、sort_word <-> counter, word, scoreみたいに辞書にしたらよかったのか。一元的にしか繋げられない辞書は避けるべきなのか
* 2次元リストを使って実装している方のコードがあったから、帰ったら計算量とか考えてどちらがいいのか評価してみたい
* ファイルの読み込み出力をきちんと自分の手で書いてみる
* 入力を正規化する方法とかもたくさんあるなら練習する

## [Case1 (Anagram2)](https://github.com/Rei-0a/STEP/blob/main/01_Anagram/Anagram_02.py)

1.[辞書の形式](https://github.com/Rei-0a/STEP/blob/main/01_Anagram/Anagram_02.py#L31)

* countedDictionaryを[[alphabetCount]*wordの数]の形式の二重リストにしている。
* alphabetCountは[aの数,bの数, ,,, zの数, 元のword, score]という形で保存し、どの単語についてもaの数が[0]、元のwordが[26], scoreは[27]に格納されている
* 私のコードみたいにdictionaryをいくつも作ることなく(sort_word <-> word, sort_word <-> score, sort_word <-> counter) 一つだけにまとめられる(counter <-> word <-> score)。

2.[高スコアのものを出力する方法](https://github.com/Rei-0a/STEP/blob/main/01_Anagram/Anagram_02.py#L47)
* 辞書をスコア順に並べてしまえばいい。なるほど！

3.[文字列を作れるかの判定](https://github.com/Rei-0a/STEP/blob/main/01_Anagram/Anagram_02.py#L52)
* inputについてもalpabetCountのようなリストを作成して比べる。
* ここでどの単語についてもaの数が[0]、元のwordが[26], scoreは[27]の決まった場所に格納されていることと辞書をスコア順に並べるのが生きる！
* 全ての要素が足りていたら,[26]を出力しその場でreturn
* 元の文字列と同じものを排除する機能はない？のかな
* もうこのreturnの時点でalphabetCount全体ではなく[26]を出力してもいいんじゃないか？

4.[入力について](https://github.com/Rei-0a/STEP/blob/main/01_Anagram/Anagram_02.py#L84)
* 正規表現を利用している
* 入力された文字列から文字（アルファベット）だけを抽出し、小文字に変換してアルファベット順に並べ替える処理を行っています

5.[ファイルの読み込みや書き出しについて](https://github.com/Rei-0a/STEP/blob/main/01_Anagram/Anagram_02.py#L25)
* `r` は **読み込みモード (read mode)** を意味します。このモードでファイルを開くと、そのファイルからデータを読み取ることができます。
* `w` (書き込みモード): ファイルにデータを書き込みます。ファイルが存在しない場合は新しく作成され、すでに存在する場合は内容がすべて上書きされます。
* `a` (追記モード): ファイルにデータを追記します。ファイルが存在しない場合は新しく作成され、すでに存在する場合は既存の内容の末尾にデータが追加されます。
