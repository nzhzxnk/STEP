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
### 1. FreeListBinをきちんと実装する！

### 方針とコード
* all_list: free_blockもallocated_blockを両方address順に繋げる。双方向連結リスト。
* bin_list: free_blockだけを繋げる。大きさごとに分けるFree List Binを組み合わせる。双方向連結リスト。
* mallocの時に前後を繋ぎ直してall_listをアドレス順にした。
* FreeListBinでは、1つのbinしか探索しないのではなくそれより大きいサイズのbinも探すようにした。
* Best FitとFirst Fitの両方を実装して比較したが、bin自体は大きさ順に並んでいるのでそこまで変わらないかと思った。
* mergeの処理を修正した。
* [malloc_bm_flb](https://github.com/nzhzxnk/STEP/blob/main/week7_homework/malloc/malloc_bm_flb.c)

### 結果
* Best fit
---
| Allocator | Time1 (ms) | Util1 (%) | Time2 (ms) | Util2 (%) | Time3 (ms) | Util3 (%) | Time4 (ms) | Util4 (%) | Time5 (ms) | Util5 (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| simple_malloc.c | 7 | 70 | 5 | 40 | 102 | 9 | 23645 | 15 | 13719 | 15 |
| malloc_bf_bm.c (Best Fit) | 1640 | 65 | 1194 | 31 | 1302 | 44 | 8209 | 71 | 5979 | 75 |
| malloc_bm_flb.c (Best Fit) | 380 | 57 | 238 | 20 | 243 | 30 | 235 | 74 | 189 | 75 |
---
* First fit
| Allocator | Time1 (ms) | Util1 (%) | Time2 (ms) | Util2 (%) | Time3 (ms) | Util3 (%) | Time4 (ms) | Util4 (%) | Time5 (ms) | Util5 (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| simple_malloc.c | 7 | 70 | 5 | 40 | 102 | 9 | 23645 | 15 | 13719 | 15 |
| malloc_ff.c (First Fit) | 9 | 65 | 9 | 31 | 123 | 8 | 27079 | 15 | 19152 | 15 |
| malloc_bm_flb.c (First Fit) | 24 | 57 | 12 | 20 | 18 | 29 | 100 | 72 | 75 | 74 |
---

### 考察
* metadataのサイズが、8bit*6=48bitもあるのでUtilityは落ちた -> metadataのサイズを減らすべき
* addressを探すのではなく繋ぎ直すことで、実行時間はかなり早くなった！
* Best FitとFirst Fitについては、やはりFirst Fitの方が早かった。ただ予想していた通り、bin自体は大きさ順に並んでいるのでどちらも早く処理できていた。

### 2. metadataを小さくする

### 方針とコード
* unionを利用し、bin_listのポインタをfreeのときだけ確保するようにした。allocatedの時はそこにユーザーのデータが書き込まれる。
* メモリのアライメント: メモリのサイズは必ず8の倍数や16の倍数に切り上げてから領域を割り当てられる。下2-3桁は必ず0になっているのでそれを間借りすればいい！
* sizeとis_allocatedを1つのsize_and_flagという変数で管理することで、16bit->8bitに削減した。
* sizeとフラグはbit演算を行うヘルパー関数を用いて算出した。
* [malloc_bm_flb_2](https://github.com/nzhzxnk/STEP/blob/main/week7_homework/malloc/malloc_bm_flb_2.c)

### 結果
* Best fit
---
| Allocator | Time1 (ms) | Util1 (%) | Time2 (ms) | Util2 (%) | Time3 (ms) | Util3 (%) | Time4 (ms) | Util4 (%) | Time5 (ms) | Util5 (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| simple_malloc.c | 7 | 70 | 5 | 40 | 102 | 9 | 23645 | 15 | 13719 | 15 |
| malloc_bf_bm.c (Best Fit) | 1640 | 65 | 1194 | 31 | 1302 | 44 | 8209 | 71 | 5979 | 75 |
| malloc_bm_flb.c (Best Fit) | 380 | 57 | 238 | 20 | 243 | 30 | 235 | 74 | 189 | 75 |
| malloc_bm_flb_2.c (Best Fit) | 274 | 60 | 219 | 22 | 180 | 33 | 167 | 75 | 152 | 76 |
---
* First fit
| Allocator | Time1 (ms) | Util1 (%) | Time2 (ms) | Util2 (%) | Time3 (ms) | Util3 (%) | Time4 (ms) | Util4 (%) | Time5 (ms) | Util5 (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| simple_malloc.c | 7 | 70 | 5 | 40 | 102 | 9 | 23645 | 15 | 13719 | 15 |
| malloc_ff.c (First Fit) | 9 | 65 | 9 | 31 | 123 | 8 | 27079 | 15 | 19152 | 15 |
| malloc_bm_flb.c (First Fit) | 24 | 57 | 12 | 20 | 18 | 29 | 100 | 72 | 75 | 74 |
| malloc_bm_flb_2.c (First Fit) | 14 | 60 | 7 | 22 | 11 | 33 | 88 | 73 | 61 | 74 |
---

### 考察
* metadataのサイズを落としたので、Utilityが少し上がった。
* 実行時間も少し上がった。
* 以前としてchallenge1,2,3のUtilityがかなり低い？結果参照

### メモリ効率をさらに上げるための工夫
* size無くしてpre,nextポインタを使って計算？、後ろにサイズを記録しておく？
* もう一度聞きたいです、、
