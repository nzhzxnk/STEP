# Week1_Anagram


## 各フォルダの説明

### `week1_anagram1_1`

辞書内の単語をソートしたものと元の単語を対応させた辞書（`ang_dict`）を事前に作成し、クエリごとにソートした文字列で辞書を検索することでアナグラムを見つけます。

**計算量**: <span class="math-inline">O\(n \\cdot m \\log m \+ q \\cdot m \\log m\)</span>
* <span class="math-inline">n</span>: 辞書の文字列 (word) の数
* <span class="math-inline">m</span>: 文字列 (word, string) の平均の長さ
* <span class="math-inline">q</span>: クエリ数

**詳細**:
* `words.txt` からソート済み単語と元の単語が対応する `ang_dict` を作成: <span class="math-inline">O\(n \\cdot m \\log m\)</span>
* 文字列の入力を `string` で受け取り、ソートして `sort_string` を作成: <span class="math-inline">O\(q \\cdot m \\log m\)</span>
* `ang_dict` のキーに `sort_string` が含まれるかを探索: <span class="math-inline">O\(q \\cdot 1\)</span>
* 元の `string` 以外のすべてのアナグラムを出力: <span class="math-inline">O\(q \\cdot 7\)</span> (`ang_dict` の値の要素は最大7つ)

### `week1_anagram1_2`

辞書内の単語をソートしたものと元の単語をタプルにしたリスト（`ang_list`）を事前に作成し、ソートされたリストに対して二分探索を行うことでアナグラムを見つけます。

**計算量**: <span class="math-inline">O\(n \\cdot m \\log m \+ n \\log n \+ q \\cdot m \\log m \+ q \\cdot \\log n\)</span>
* <span class="math-inline">n</span>: 辞書の文字列 (word) の数
* <span class="math-inline">m</span>: 文字列 (word, string) の平均の長さ
* <span class="math-inline">q</span>: クエリ数

**詳細**:
* `words.txt` からソート済み単語と元の単語をタプルにした `ang_list` を作成: <span class="math-inline">O\(n \\cdot m \\log m \+ n \\log n\)</span>
* 文字列の入力を `string` で受け取り、ソートして `sort_string` を作成: <span class="math-inline">O\(q \\cdot m \\log m\)</span>
* ソート順になっている `ang_list` を二分探索し、`sort_string` が `ang_list` にあった場合に入る場所をインデックスで返す: <span class="math-inline">O\(q \\cdot \\log n\)</span>
* `ang_list` のタプル第一要素 (`sort_word`) が `sort_string` と一致する間のみ探索を続け、そのうち第二要素 (`word`) が `string` と一致しないもののみを出力: <span class="math-inline">O\(q \\cdot 7\)</span> (アナグラム同士である辞書内の要素は最大7つ)

### `week1_anagram2_1`

与えられた文字列の全ての文字を使わなくてもアナグラムとして認めます。
文字ごとにスコアが設定されており、最大スコアを持つアナグラムを探索します。`collections.Counter` 関数を使わずに実装されています。

* 入力: `small.txt`, `medium.txt`, `large.txt`
* 出力: 各単語について「最大のスコアを持つアナグラム」を列挙したファイル

**文字のスコア**:
* 1点: `a`, `e`, `h`, `i`, `n`, `o`, `r`, `s`, `t`
* 2点: `c`, `d`, `l`, `m`, `u`
* 3点: `b`, `f`, `g`, `p`, `v`, `w`, `y`
* 4点: `j`, `k`, `q`, `x`, `z`

**詳細**:
* `ang_dict` を元に、`score_dict` (ソート済み単語と単語のスコア) と `counter_dict` (ソート済み単語と文字の出現回数) を作成します。
* 辞書がソート済みであることを利用し、`for` ループで各要素の種類と数を計上し `counter_dict` を作成します。
* 入力 (`string`) を受け取りソートして、`string_counter` を作成します。
* `string_counter` と `word_counter` の差分が `False` (つまり `word_counter` が `string_counter` に含まれている) かつ `word_score` が最大のものを出力します。

## 各ファイルの役割

* `main.py`: プログラムのメイン実行ファイルです。
* `dictionary.py`: 主に辞書を作成する関数（`ang_dict`、`counter_dict`、`score_dict`など）が定義されています。
* `test.py`: テストケースとそれを実行するファイルです。
* `search.py`: 二分探索の関数が定義されています。（`week1_anagram1_2` で使用）
* `other.py`: `main.py` に間接的に関わるその他の関数が定義されています。

## プログラムの実行方法

プログラムを実行する場合は、各ディレクトリ内の `main.py` ファイルを実行してください。

```bash
python main.py
