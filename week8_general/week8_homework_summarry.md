## Week7 Homework(malloc challenge)
---
### 内容
* malloc.c 内の malloc ロジックを改善し、速度とメモリ使用量を向上させる！
* 詳しくは[week7_homework_summary]()を参照
-----
### 前回からの反省点
* FreeListBinの実装で、1つのbinしか探索していないから処理が終わらないことがわかった。
* mergeとFreeListBinを組み合わせる時、sizeの変更に合わせて所属するbinも変更しなければならないことのに、元のbinに存在したままになっていたことで無限ループが発生していた。
* address順に連結リストを全て辿って挿入場所を確認していたので膨大な時間がかかっていたが、そんなことしなくてもmallocの時に前後を繋ぎ直せばよかった。
* metadataのサイズが、Utilityに大きく関わることがわかった
* HashTableのリハッシュのようにfree_blockを全て左側に移動しまとめる処理はC言語ではできないとわかった

-----
### 方針とコード
* all_list: free_blockもallocated_blockを両方address順に繋げる。双方向連結リスト。
* mergeの際にはall_listの前または後のフラグがfreeであることを確認すれば良い。
* allocated_blockの右にfree_bolockがあったらそれらを入れ替えるのを繰り返せば、全てのfree_blockが左に寄せられると考えた。
* bin_list: free_blockだけを繋げる。大きさごとに分けるFree List Binを組み合わせる。双方向連結リスト。
* [malloc_bm_flb](https://github.com/nzhzxnk/STEP/blob/main/week7_homework/malloc/malloc_bm_flb.c)

### 結果


### 考察
* 連結リストを単に追加順に並べた時よりaddress順にした方がメモリの効率は上がった。
* 連結リストに追加する際に線形探索をするので、実行時間が長くなってしまうかと予想していたが、大規模なテストケースでもそのような問題は見られなかった。


### メモリ効率をさらに上げるための工夫



## 改善すべき点
* matadataの中のデータをなるべく減らす。size 64bitもいらん int16とか使えばいい？
* 全部辿ってcurrとnextを繋ぎ直せば頭から辿る必要はない
* gerbage collector
* mark and skip copying gc compaction 辿り着けなくなったやつを消す
右隣のメモリを参照するときに、そのメモリが今回私が触っていいメモリなのかということの確認をしないと、全く関係のないファイルが保持しているメモリを書き換えてしまう可能性が出てくる。
* binが綺麗に分散するように分ける
* 不要なページをリターン？
* "ポインタ+ポインタ"はコンパイルエラー