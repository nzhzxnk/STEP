
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
