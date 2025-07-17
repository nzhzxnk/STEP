## Week7 Homework(malloc challenge)
---
### 内容
malloc.c 内の malloc ロジックを改善し、速度とメモリ使用量を向上させる！

---
### ベンチマークのビルドと実行方法
以下のコマンドでビルドとベンチマークの実行が可能です。
1. このリポジトリをクローンする
git clone https://github.com/hikalium/malloc_challenge.git
2. malloc ディレクトリに移動する
cd malloc_challenge
cd malloc
3. ビルドする
make
4. ベンチマークを実行する（スコアボード用）
make run
5. トレース用の小規模なベンチマークを実行する（スコアボード用ではなく、視覚化とデバッグ目的のみ）
make run_trace

-----
## 1. Fitの方法を考える

### 方針とコード
* First_fit, Worst_fit, Best_fitを実装し、最適な方法を比較する
* [malloc.c(First_fit)](https://github.com/nzhzxnk/STEP/blob/main/week7_homework/malloc/malloc.c)
* [malloc_bf.c(Best_fit)](https://github.com/nzhzxnk/STEP/blob/main/week7_homework/malloc/malloc_bf.c)
* [malloc_wf.c(Worst_fit)](https://github.com/nzhzxnk/STEP/blob/main/week7_homework/malloc/malloc_wf.c)

### 結果
---
#### Challenge #1
| 項目            | First_fit | Best_fit | worst_fit  |
| :-------------- | :------------ | :------------- | :------------- |
| Time [ms]       | 10            | 1592           | 1582           |
| Utilization [%] | 70            | 70             | 70             |
---
#### Challenge #2
| 項目            | First_fit | Best_fit | worst_fit |
| :-------------- | :------------ | :------------- | :------------- |
| Time [ms]       | 7             | 1112           | 1166           |
| Utilization [%] | 40            | 40             | 40             |
---
#### Challenge #3
| 項目            | First_fit | Best_fit | worst_fit |
| :-------------- | :------------ | :------------- | :------------- |
| Time [ms]       | 127           | 1334           | 68286          |
| Utilization [%] | 9             | 51             | 4              |
---
#### Challenge #4
| 項目            | First_fit | Best_fit | worst_fit |
| :-------------- | :------------ | :------------- | :------------- |
| Time [ms]       | 24397         | 9465           | 849108         |
| Utilization [%] | 15            | 72             | 7              |
---
#### Challenge #5
| 項目            | First_fit | Best_fit | worst_fit |
| :-------------- | :------------ | :------------- | :------------- |
| Time [ms]       | 17133         | 6121           | 705569         |
| Utilization [%] | 15            | 75             | 7              |
---

### 考察
* 固定長のテストケース(Challenge1,2)ではどの方法でもメモリ効率に変化はなく, 実行時間はFirst_Fitが圧倒的に短かった。
* ランダムな長さが与えられるテストケース(Challenge3,4,5)では, Best_fitが最もメモリ効率がよいという結果になった。
* 実行時間についても、Challenge3を除きBest_fitが最も短いという結果になった。
* First_fitは小規模または固定長のケースには適しているが、その他のケースではBest_fitが最適であると考えた。

-----
## 2. free_blockのmergeをする

### 方針とコード
* free_listのポインターをたどって、もしアドレスが隣り合っていたらmergeする。
* Challenge1,2はFirst_fitで、Callenge3,4,5はBest_fitで実行する。
* mergeするタイミングは、allocatedであった空間が解放されてfreeになるとき(my_free)と新たなメモリを追加する時(mmap_from_system)に限られるので、その関数の処理が終わったらmergeすることにした。
* ポインタと次のポインタが指す領域が、メモリ上でも物理的に隣り合っているfree_blockである場合に、mergeが成立することになっている。
* both_mergeでは連結リストを双方向にして、prevとnextにすぐアクセスできるように工夫した。
* [malloc_ff_rm(First_fit, 右側のみ結合)](https://github.com/nzhzxnk/STEP/blob/main/week7_homework/malloc/malloc_ff_rm.c)
* [malloc_ff_rm(First_fit, 両側結合)](https://github.com/nzhzxnk/STEP/blob/main/week7_homework/malloc/malloc_ff_bm.c)
* [malloc_bf_rm(Best_fit, 右側のみ結合)](https://github.com/nzhzxnk/STEP/blob/main/week7_homework/malloc/malloc_bf_rm.c)
* [malloc_bf_bm(Best_fit, 両側結合)](https://github.com/nzhzxnk/STEP/blob/main/week7_homework/malloc/malloc_bf_bm.c)

### 結果
---
#### Challenge #1
| 項目            | no_merge(simple_malloc) | both_merge | right_merge |
| :-------------- | :------------ | :---------- | :--------- |
| Time [ms]       | 10            | 9        | 11          |
| Utilization [%] | 70            | 65          | 70         |
---
#### Challenge #2
| 項目            | no_merge(simple_malloc) | both_merge | right_merge |
| :-------------- | :------------ | :---------- | :--------- |
| Time [ms]       | 7             | 9        | 7          |
| Utilization [%] | 40            | 31          | 40         |
---
#### Challenge #3
| 項目            | simple_malloc | no_merge | both_merge | right_merge |
| :-------------- | :------------ | :------- | :--------- | :---------- |
| Time [ms]       | 129           | 1334     | 1302       | 1350        |
| Utilization [%] | 9             | 51       | 44         | 51          |
---
#### Challenge #4

| 項目            | simple_malloc | no_merge | both_merge | right_merge |
| :-------------- | :------------ | :------- | :--------- | :---------- |
| Time [ms]       | 12488         | 9465     | 8209       | 9671        |
| Utilization [%] | 15            | 72       | 71         | 72          |
---
#### Challenge #5
| 項目            | simple_malloc | no_merge | both_merge | right_merge |
| :-------------- | :------------ | :------- | :--------- | :---------- |
| Time [ms]       | 11758         | 6121     | 5079       | 6017        |
| Utilization [%] | 15            | 75       | 75         | 75          |
---

### 考察
* both_mergeの方がno_merge, right_mergeに比べメモリ効率が下がる、または変化しないという結果となった。
* 実行時間はboth_mergeが最も早く、テストケースが大規模になるにつれ差が顕著になっていた。
* 現在のポインターの繋ぎ方は、新しく追加したものをheadに繋げていく方法であり、ポインタと次のポインタが指す領域がメモリ上でも物理的に隣り合っているfree_blockである場合に、mergeが成立することになっている。
* そのようなケースは非常に稀で、ほとんどの隣り合う空間がmergeされないことが原因である可能性を考えた。
* もしかしたらきちんとマージされていないのかも、確認する方法を考えたい。

-----
## 3. mergeの効率を上げるために連結リストの順番を工夫する

### 方針とコード
* ポインタと次のポインタが指す領域が、メモリ上でも物理的に隣り合っているfree_blockである場合というのは稀であるため、mergeしても効率が上がらなかったと仮定する。
* free_listを追加順ではなくaddress順に繋げることでこの問題を解決できると考えた。
* [malloc_bf_bm_ad](https://github.com/nzhzxnk/STEP/blob/main/week7_homework/malloc/malloc_bf_bm_ad.c)

### 結果
---
#### Challenge #3
| 項目            | both_merge | address |
| :-------------- | :--------- | :------ |
| Time [ms]       | 1302       | 1050    |
| Utilization [%] | 44         | 44      |
---
#### Challenge #4
| 項目            | both_merge | address |
| :-------------- | :--------- | :---------- |
| Time [ms]       | 8209       | 8310        |
| Utilization [%] | 71         | 73          |
---
#### Challenge #5
| 項目            | both_merge | address |
| :-------------- | :--------- | :---------- |
| Time [ms]       | 5079       | 4656        |
| Utilization [%] | 75         | 76          |
---

### 考察
* 連結リストを単に追加順に並べた時よりaddress順にした方がメモリの効率は上がった。
* 連結リストに追加する際に線形探索をするので、実行時間が長くなってしまうかと予想していたが、大規模なテストケースでもそのような問題は見られなかった。

-----
## 4. メモリ効率を上げるために連結リストを工夫する

### 方針とコード
* free_listを大きさごとに複数に分けて保存する(Free List Bin)を実装しないとこれ以上メモリ効率は上がらないと考えた
* [malloc_bf_bm_flb](https://github.com/nzhzxnk/STEP/blob/main/week7_homework/malloc/malloc_bf_bm_flb.c)

### 結果
* エラーは起きないがずっと結果が表示されない、、原因の場所はわかったが直せてはいない

### 考察
* lldbでデバックしたらここでループ？しているらしかった
```c[]
void my_add_new_memory()
{
  size_t buffer_size = 4096;
  my_metadata_t *new_metadata =
      (my_metadata_t *)mmap_from_system(buffer_size);
  new_metadata->size = buffer_size - sizeof(my_metadata_t);
  new_metadata->next = NULL;
  new_metadata->prev = NULL;
  my_add_to_free_list(new_metadata); // 新たに追加された領域をfree_listに追加する
}
```
-----
## 5. メモリ効率をさらに上げるための工夫

### 方針
* sizeに適合するfree_blockが見つからなかったらすぐにadd_new_memoryを呼び出すのではなく、HashTableのリハッシュのようにfree_blockを全て左側に移動しまとめる処理を挟めば、メモリ効率をもっと上げることができるのではないかと考えた。
* all_list: free_blockもallocated_blockを両方address順に繋げる。双方向連結リスト。
* mergeの際にはall_listの前または後のフラグがfreeであることを確認すれば良い。
* allocated_blockの右にfree_bolockがあったらそれらを入れ替えるのを繰り返せば、全てのfree_blockが左に寄せられると考えた。
* bin_list: free_blockだけを繋げる。大きさごとに分けるFree List Binを組み合わせる。双方向連結リスト。
* [malloc_bf_bm_ad_flb](https://github.com/nzhzxnk/STEP/blob/main/week7_homework/malloc/malloc_bf_bm_flb_ad.c)

### 結果
* エラーは起きないがずっと結果が表示されない、、原因の場所はわかったが直せてはいない

### 考察
* flb単体もできていないのでやはり実装に問題がああるか？
* ポインタを追うデバックをしてadd_all_listでの無限ループがあることがわかり、それは解消したが未だ実行終わらない
* allocated_blockを含めるようにしたので単純にポインタに繋げる量が多くて、さらにaddress順にしているので、かなり膨大な処理になっているのかも、、

## 改善すべき点
* matadataの中のデータをなるべく減らす。size 64bitもいらん int16とか使えばいい？
* 全部辿ってcurrとnextを繋ぎ直せば頭から辿る必要はない
* gerbage collector
* mark and skip copying gc compaction 辿り着けなくなったやつを消す
右隣のメモリを参照するときに、そのメモリが今回私が触っていいメモリなのかということの確認をしないと、全く関係のないファイルが保持しているメモリを書き換えてしまう可能性が出てくる。
* binが綺麗に分散するように分ける
* 不要なページをリターン？
* "ポインタ+ポインタ"はコンパイルエラー