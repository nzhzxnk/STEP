#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define NUM_BINS 10 // ビンの数。サイズクラスに応じて決定

/* Interfaces to get memory pages from OS */

void *mmap_from_system(size_t size);
void munmap_to_system(void *ptr, size_t size);

/* Struct definitions */

typedef struct my_metadata_t // address順にfree_blockとallocated_blockを双方向連結リストにして保存
{
  size_t size;
  bool is_allocated; // この領域が割り当て済みかどうかを示すフラグ
  struct my_metadata_t *all_next;
  struct my_metadata_t *all_prev; // 双方向リストにする
  struct my_metadata_t *bin_next;
  struct my_metadata_t *bin_prev; // 双方向リストにする
} my_metadata_t;

typedef struct my_heap_t
{
  // all_list用
  my_metadata_t *all_head;
  my_metadata_t all_dummy_head; // リストの先頭のダミーノード
  my_metadata_t all_dummy_tail; // リストの末尾のダミーノード

  // 各binごとのfree_list用
  my_metadata_t *bin_head[NUM_BINS];
  my_metadata_t bin_dummy_head[NUM_BINS];
  my_metadata_t bin_dummy_tail[NUM_BINS];
} my_heap_t;

/* Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!) */
my_heap_t my_heap;

/* Helper functions */

void my_initialize()
{
  // all_list用
  my_heap.all_dummy_head.size = 0;
  my_heap.all_dummy_head.is_allocated = false; // ダミーノードは常に空き
  my_heap.all_dummy_head.all_prev = NULL;
  my_heap.all_dummy_head.all_next = &my_heap.all_dummy_tail;
  my_heap.all_dummy_tail.size = 0;
  my_heap.all_dummy_tail.is_allocated = false; // ダミーノードは常に空き
  my_heap.all_dummy_tail.all_prev = &my_heap.all_dummy_head;
  my_heap.all_dummy_tail.all_next = NULL;
  my_heap.all_head = &my_heap.all_dummy_head; // free_listの先頭はdummy_headから始まる

  // bin_nextとbin_prevは、all_listのダミーノードでは使用しないのでNULLにしておく
  my_heap.all_dummy_head.bin_next = NULL;
  my_heap.all_dummy_head.bin_prev = NULL;
  my_heap.all_dummy_tail.bin_next = NULL;
  my_heap.all_dummy_tail.bin_prev = NULL;

  // binごとのfree_list用
  for (int i = 0; i < NUM_BINS; i++)
  {
    my_heap.bin_dummy_head[i].size = 0;
    my_heap.bin_dummy_head[i].is_allocated = false; // ダミーノードは常に空き
    my_heap.bin_dummy_head[i].bin_prev = NULL;
    my_heap.bin_dummy_head[i].bin_next = &my_heap.bin_dummy_tail[i];
    my_heap.bin_dummy_tail[i].size = 0;
    my_heap.bin_dummy_tail[i].is_allocated = false; // ダミーノードは常に空き
    my_heap.bin_dummy_tail[i].bin_prev = &my_heap.bin_dummy_head[i];
    my_heap.bin_dummy_tail[i].bin_next = NULL;
    my_heap.bin_head[i] = &my_heap.bin_dummy_head[i]; // free_listの先頭はdummy_headから始まる

    // all_nextとall_prevは、ビンリストのダミーノードでは使用しないのでNULLにしておく
    my_heap.bin_dummy_head[i].all_next = NULL;
    my_heap.bin_dummy_head[i].all_prev = NULL;
    my_heap.bin_dummy_tail[i].all_next = NULL;
    my_heap.bin_dummy_tail[i].all_prev = NULL;
  }
}

int my_get_bin_index(size_t size)
{ // bin_indexを決定する関数
  if (size <= 8)
    return 0; // switch文はラベルに範囲を設定できない
  if (size <= 16)
    return 1;
  if (size <= 32)
    return 2;
  if (size <= 64)
    return 3;
  if (size <= 128)
    return 4;
  if (size <= 256)
    return 5;
  if (size <= 512)
    return 6;
  if (size <= 1024)
    return 7;
  if (size <= 2048)
    return 8;
  return NUM_BINS - 1;
  // Challenge 1: run_challenge("trace1_my.txt", 128, 128, ...) min_size = 128, max_size = 128
  // Challenge 2: run_challenge("trace2_my.txt", 16, 16, ...) min_size = 16, max_size = 16
  // Challenge 3: run_challenge("trace3_my.txt", 16, 128, ...) min_size = 16, max_size = 128, 指数分布, 出現回数は16>>128
  // Challenge 4: run_challenge("trace4_my.txt", 256, 4000, ...) min_size = 256, max_size = 4000, 指数分布, 出現回数は256>>4000
  // Challenge 5: run_challenge("trace5_my.txt", 8, 4000, ...), min_size = 8, max_size = 4000, 指数分布, 出現回数は256>>4000
}

void my_add_to_bin_list(my_metadata_t *metadata)
{ // binリストにfree_blockを追加
  assert(!metadata->is_allocated);
  assert(!metadata->bin_next && !metadata->bin_prev);

  int bin_index = my_get_bin_index(metadata->size); // サイズから適切なビンを決定
  // 特に順番は関係なさそうなので前に追加していく方式で
  metadata->bin_next = my_heap.bin_head[bin_index]->bin_next;
  metadata->bin_prev = my_heap.bin_head[bin_index];
  metadata->bin_next->bin_prev = metadata;
  my_heap.bin_head[bin_index]->bin_next = metadata;
}

void my_add_to_all_list(my_metadata_t *metadata)
{
  assert(!metadata->all_next && !metadata->all_prev);

  my_metadata_t *current = &my_heap.all_dummy_head;

  // metadataのアドレスが current->all_next のアドレスよりも大きくなるまで current を進める
  // このループ後、metadata は current と current->all_next の間に挿入されるべき
  // current->all_next がダミーテールであるか、または metadata のアドレスが current->all_next のアドレスより小さい場合、ループを終了する
  while (current->all_next != &my_heap.all_dummy_tail &&
         (uintptr_t)current->all_next < (uintptr_t)metadata)
  {
    // printf("Searching for insertion point: current=%p, current->all_next=%p, metadata=%p\n",
    //        (void*)current, (void*)current->all_next, (void*)metadata);
    current = current->all_next;
  }

  // ここに到達した時、current は metadata が挿入されるべき直前のノードを指している

  assert(current != metadata);

  // リストへの挿入処理
  metadata->all_next = current->all_next; // 新しいノードの next は current の次のノード
  metadata->all_prev = current;           // 新しいノードの prev は current
  current->all_next->all_prev = metadata;
  current->all_next = metadata;

  // printf("Inserted metadata=%p: prev=%p, next=%p\n",
  //        (void*)metadata, (void*)metadata->all_prev, (void*)metadata->all_next);
}

// void my_add_to_all_list(my_metadata_t *metadata)
// {
//   assert(!metadata->all_next && !metadata->all_prev);

//   my_metadata_t *current = &my_heap.all_dummy_head;

//   // metadataのアドレスがcurrent->all_nextのアドレスよりも大きくなるまで進む
//   // currentはmetadataの物理的な前、または挿入位置になるはずのノード
//   // このループ後、metadata は current と current->all_next の間に挿入されるべき
//   while ((uintptr_t)current < (uintptr_t)metadata)
//   {
//     my_metadata_t *final = my_heap.all_dummy_tail.all_prev;
//     printf("current: %p, current->all_next: %p, metadata: %p, final: %p\n", current, current->all_next, metadata, final);
//     if (current->all_next == &my_heap.all_dummy_tail){break;}
//     current = current->all_next;

//   }
//   assert(current != metadata);
//   metadata->all_next = current->all_next;
//   metadata->all_prev = current;
//   printf("current->all_next : %p",current->all_next);
//   current->all_next->all_prev = metadata;
//   current->all_next = metadata;
// }

void my_remove_from_all_list(my_metadata_t *metadata)
{ // 基本all_listの要素は削除されないが,mergeでfree_listが結合した時にだけ使う
  assert(!metadata->is_allocated);
  assert(metadata->all_prev != NULL && metadata->all_next != NULL); // ダミーノードでないことを確認

  metadata->all_prev->all_next = metadata->all_next;
  metadata->all_next->all_prev = metadata->all_prev;
  // 削除されたノードのポインタをクリア
  metadata->all_next = NULL;
  metadata->all_prev = NULL;
}

void my_remove_from_bin_list(my_metadata_t *metadata)
{
  int bin_index = my_get_bin_index(metadata->size); // サイズから適切なビンを決定
  // ダミーノードは削除しない
  assert(metadata != &my_heap.bin_dummy_head[bin_index]);
  assert(metadata != &my_heap.bin_dummy_tail[bin_index]);

  // prevとnext同士を繋ぐ
  metadata->bin_prev->bin_next = metadata->bin_next;
  metadata->bin_next->bin_prev = metadata->bin_prev;
  // 削除されたノードのポインタをクリア
  metadata->bin_next = NULL;
  metadata->bin_prev = NULL;
}

void my_merge_free_block(my_metadata_t *metadata)
{
  assert(!metadata->is_allocated); // 基本metadataがfreeの時しかmerge呼び出さない
                                   // assert(metadata->all_next == (my_metadata_t *)((char *)metadata + sizeof(my_metadata_t) + metadata->size));
                                   // assert(metadata == (my_metadata_t *)((char *)metadata->all_prev + sizeof(my_metadata_t) + metadata->all_prev->size));
  bool is_head = true;

  // all_listを辿ったnextのフラグもfalseなら結合
  if (!metadata->all_next->is_allocated && metadata->all_next != &my_heap.all_dummy_tail)
  {
    my_metadata_t *next_node_to_merge = metadata->all_next;
    my_remove_from_all_list(metadata->all_next);                        // next_metadataをフリーリストから削除し、free_listを繋ぎ直す
    my_remove_from_bin_list(metadata->all_next);                        // next_metadataをフリーリストから削除し、free_listを繋ぎ直す
    metadata->size += sizeof(my_metadata_t) + next_node_to_merge->size; // 解放ブロックのサイズを、隣の空きブロックのサイズとメタデータ分だけ増やす
  }
  // all_listを辿ったnextのフラグもfalseなら結合
  if (!metadata->all_prev->is_allocated && metadata->all_prev != &my_heap.all_dummy_head)
  {
    my_metadata_t *prev_node_to_merge = metadata->all_prev;
    my_remove_from_all_list(metadata);                                  // metadataをフリーリストから削除し、free_listを繋ぎ直す
    my_remove_from_bin_list(metadata);                                  // next_metadataをフリーリストから削除し、free_listを繋ぎ直す
    prev_node_to_merge->size += sizeof(my_metadata_t) + metadata->size; // 解放ブロックのサイズを、隣の空きブロックのサイズとメタデータ分だけ増やす
    is_head = false;
  }
  if (is_head)
  {
    my_add_to_bin_list(metadata);
  }
}

void my_add_new_memory()
{
  size_t buffer_size = 4096;
  my_metadata_t *new_metadata = (my_metadata_t *)mmap_from_system(buffer_size);
  new_metadata->size = buffer_size - sizeof(my_metadata_t);
  new_metadata->is_allocated = false;
  new_metadata->all_next = NULL;
  new_metadata->all_prev = NULL;
  new_metadata->bin_next = NULL;
  new_metadata->bin_prev = NULL;
  my_add_to_all_list(new_metadata); // 新たに追加された領域をall_listに追加する
  my_add_to_bin_list(new_metadata); // 新たに追加された領域をfree_listに追加する
}

/* Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!) */

void *my_malloc(size_t size)
{
  int bin_index = my_get_bin_index(size);
  my_metadata_t *metadata = my_heap.bin_head[bin_index]->bin_next; // free_listの先頭ポインタ
  // Best-fit: Find the smallest free slot that fits the object.
  my_metadata_t *best_fit_metadata = NULL; // 最適なfree_blockのmetadataを指すポインタ
  size_t min_diff = (size_t)-1;            // size_t(符号なし整数型)が取れる最大値で初期化。
  // モジュロ演算（剰余演算）で-1は全てのビットが1であると表現されるので最大値になる。

  while (metadata != &my_heap.bin_dummy_tail[bin_index]) // ダミーテールまで走査
  {
    assert(!metadata->is_allocated);
    if (metadata->size >= size)
    { // 要求されたsizeを満たすブロックである場合
      size_t current_diff = metadata->size - size;
      if (current_diff <= min_diff)
      { // かつ現時点でのfree_blockの最小値以下の場合、best_fit_metadata, best_fit_prev, min_diffを更新
        best_fit_metadata = metadata;
        min_diff = current_diff;
      }
    }
    metadata = metadata->bin_next; // metadataを次の要素へ更新
  }
  // ループが終了後のbest_fit_metadata, best_fit_prevが最適なfree_blockの情報なので、meatadata, prevにアドレスを代入
  metadata = best_fit_metadata;

  // 最適な空きスロットが見つからなかった場合、新たなメモリをOSにお願いする(void *mmap_from_system)
  if (!metadata)
  {
    my_add_new_memory();    // 新たなメモリを追加し、free_listに繋げる
    return my_malloc(size); // 新たなメモリ領域を確保したので再帰で呼び出し
  }

  // メモリの割り当て
  metadata->is_allocated = true; // ptr(割り当てる領域の開始アドレス)はmetadataの次のアドレス
  my_remove_from_bin_list(metadata);
  void *ptr = metadata + 1;
  size_t remaining_size = metadata->size - size;
  if (remaining_size > sizeof(my_metadata_t)) // my_metadata_tが入る大きさ分の残りサイズがある場合のみ、残りをfree_listに繋げる
  {
    metadata->size = size;
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->is_allocated = false;
    new_metadata->all_next = NULL;
    new_metadata->all_prev = NULL;
    new_metadata->bin_next = NULL;
    new_metadata->bin_prev = NULL;
    my_add_to_bin_list(new_metadata); // 新たに追加された領域をfree_listに追加する
    my_add_to_all_list(new_metadata); // 新たに追加された領域をfree_listに追加する
  }
  return ptr; // ptr(割り当てる領域の開始アドレス)を返す
}

void my_free(void *ptr)
{
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  metadata->is_allocated = false;
  metadata->bin_next = NULL;
  metadata->bin_prev = NULL;
  my_merge_free_block(metadata);
}

// This is called at the end of each challenge.
void my_finalize()
{
  // Nothing is here for now.
  // feel free to add something if you want!
}

void test()
{
  // Implement here!
  assert(1 == 1); /* 1 is 1. That's always true! (You can remove this.) */
}

// RESULT
//実行時間長すぎて使い物にならない