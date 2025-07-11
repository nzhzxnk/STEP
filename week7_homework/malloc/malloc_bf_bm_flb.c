//
// >>>> malloc challenge! <<<<
//
// Your task is to improve utilization and speed of the following malloc
// implementation.
// Initial implementation is the same as the one implemented in simple_malloc.c.
// For the detailed explanation, please refer to simple_malloc.c.

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define NUM_BINS 10 // ビンの数。サイズクラスに応じて決定

//
// Interfaces to get memory pages from OS
//

void *mmap_from_system(size_t size);
void munmap_to_system(void *ptr, size_t size);

//
// Struct definitions
//

typedef struct my_metadata_t
{
  size_t size;
  struct my_metadata_t *next;
  struct my_metadata_t *prev; // 双方向リストにする
} my_metadata_t;

typedef struct my_heap_t
{
  // 各binごとのfree_list用
  my_metadata_t *bin_head[NUM_BINS];
  my_metadata_t bin_dummy_head[NUM_BINS];
  my_metadata_t bin_dummy_tail[NUM_BINS];
} my_heap_t;

//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//
my_heap_t my_heap;

//
// Helper functions (feel free to add/remove/edit!)
//
void my_initialize()
{
  for (int i = 0; i < NUM_BINS; i++)
  {
    my_heap.bin_dummy_head[i].size = 0;
    my_heap.bin_dummy_head[i].prev = NULL;
    my_heap.bin_dummy_head[i].next = &my_heap.bin_dummy_tail[i];
    my_heap.bin_dummy_tail[i].size = 0;
    my_heap.bin_dummy_tail[i].prev = &my_heap.bin_dummy_head[i];
    my_heap.bin_dummy_tail[i].next = NULL;
    my_heap.bin_head[i] = &my_heap.bin_dummy_head[i]; // free_listの先頭はdummy_headから始まる
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

void my_remove_from_free_list(my_metadata_t *metadata)
{
  int bin_index = my_get_bin_index(metadata->size); // サイズから適切なビンを決定
  // ダミーノードは削除しない
  assert(metadata != &my_heap.bin_dummy_head[bin_index]);
  assert(metadata != &my_heap.bin_dummy_tail[bin_index]);
  // prevとnext同士を繋ぐ
  metadata->prev->next = metadata->next;
  metadata->next->prev = metadata->prev;
  metadata->next = NULL; // 削除されたノードのポインタをクリア
  metadata->prev = NULL; // 削除されたノードのポインタをクリア
}

void *my_merge_free_list(my_metadata_t *metadata)
{
  int bin_index = my_get_bin_index(metadata->size); // サイズから適切なビンを決定
  // free_listを辿ったnext_metadataのアドレスと、metadataのfree_blockの次のブロックのアドレスが一致していれば、次もfree_blockが連続していることになる。
  if (metadata->prev != &my_heap.bin_dummy_head[bin_index] && metadata->prev != &my_heap.bin_dummy_tail[bin_index])
  {
    if (metadata->next == (my_metadata_t *)((char *)metadata + sizeof(my_metadata_t) + metadata->size))
    {
      my_metadata_t *next_node_to_merge = metadata->next;
      my_remove_from_free_list(metadata->next);                           // next_metadataをフリーリストから削除し、free_listを繋ぎ直す
      metadata->size += sizeof(my_metadata_t) + next_node_to_merge->size; // 解放ブロックのサイズを、隣の空きブロックのサイズとメタデータ分だけ増やす
    }
    // dummy.headでない場合
    // free_listを辿ったnext_metadataのアドレスと、metadataのfree_blockの次のブロックのアドレスが一致していれば、次もfree_blockが連続していることになる。
    if (metadata == (my_metadata_t *)((char *)metadata->prev + sizeof(my_metadata_t) + metadata->prev->size))
    {
      my_metadata_t *prev_node_to_merge = metadata->prev;
      my_remove_from_free_list(metadata);                                 // metadataをフリーリストから削除し、free_listを繋ぎ直す
      prev_node_to_merge->size += sizeof(my_metadata_t) + metadata->size; // 解放ブロックのサイズを、隣の空きブロックのサイズとメタデータ分だけ増やす
      metadata = prev_node_to_merge;
    }
  }
  return metadata;
}

void my_add_to_free_list(my_metadata_t *metadata)
{ // binリストにfree_blockを追加
  assert(!metadata->next && !metadata->prev);

  int bin_index = my_get_bin_index(metadata->size); // サイズから適切なビンを決定
  // 特に順番は関係なさそうなので前に追加していく方式で
  metadata->next = my_heap.bin_head[bin_index]->next;
  metadata->prev = my_heap.bin_head[bin_index];
  metadata->next->prev = metadata;
  my_heap.bin_head[bin_index]->next = metadata;
}

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

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//
void *my_malloc(size_t size)
{
  int bin_index = my_get_bin_index(size); // サイズから適切なビンを決定
  // metadata配列(free_list)の先頭と、その直前のポインタを設定
  my_metadata_t *best_fit_metadata = NULL; // 最適なfree_blockのmetadataを指すポインタ
  bool find_space = false;

  for (int i = bin_index; i < NUM_BINS; i++)
  {
    my_metadata_t *metadata = my_heap.bin_head[bin_index]; // metadata配列の先頭ポインタ
    size_t min_diff = (size_t)-1;                          // size_t(符号なし整数型)が取れる最大値で初期化。
    while (metadata)                                       // metadata配列の最後まで走査
    {
      if (metadata->size > size)
      { // 要求されたsizeを満たすブロックである場合
        find_space = true;
        size_t current_diff = metadata->size - size;
        if (current_diff < min_diff)
        { // かつ現時点でのfree_blockの最小値より小さい場合、best_fit_metadata, best_fit_prev, min_diffを更新
          best_fit_metadata = metadata;
          min_diff = current_diff;
        }
      }
      metadata = metadata->next; // metadataを次の要素へ更新
    }
    if (find_space)
    {
      break;
    }
  }
  // 最適な空きスロットが見つからなかった場合、新たなメモリをOSにお願いする(void *mmap_from_system)
  if (!best_fit_metadata)
  {
    my_add_new_memory();    // 新たなメモリを追加し、free_listに繋げる
    return my_malloc(size); // 新たなメモリ領域を確保したので再帰で呼び出し
  }

  // メモリの割り当て
  void *ptr = best_fit_metadata + 1;                      // ptr(割り当てる領域の開始アドレス)はmetadataの次のアドレス
  size_t remaining_size = best_fit_metadata->size - size; // 割り当て後の残りサイズを計算
  my_remove_from_free_list(best_fit_metadata);            // メモリを割り当て、その領域をfree_listから削除
  if (remaining_size > sizeof(my_metadata_t))             // my_metadata_tが入る大きさ分の残りサイズがある場合のみ、残りをfree_listに繋げる
  {
    best_fit_metadata->size = size;
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    new_metadata->prev = NULL;
    my_add_to_free_list(new_metadata);
  }
  return ptr; // ptr(割り当てる領域の開始アドレス)を返す
}

// This is called every time an object is freed.  You are not allowed to
// use any library functions other than mmap_from_system / munmap_to_system.
void my_free(void *ptr)
{
  // Look up the metadata. The metadata is placed just prior to the object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  metadata->next = NULL;
  metadata->prev = NULL;
  my_add_to_free_list(metadata);
  my_metadata_t *merged_metadata = my_merge_free_list(metadata);
  my_add_to_free_list(merged_metadata);
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
// 実行が終わらない、、止めるとここでやられてるらしいが未だ究明できず。
// Process 58976 launched: '/Users/hayashiayano/Desktop/STEP/week7_homework/malloc/malloc_challenge.bin' (arm64)
// Welcome to the malloc challenge!
// size_of(uint8_t *) = 8
// size_of(size_t) = 8
// Running tests...
// Finished!

// Process 58976 stopped
// * thread #1, queue = 'com.apple.main-thread', stop reason = signal SIGSTOP
//     frame #0: 0x0000000100003200 malloc_challenge.bin`my_malloc [inlined] my_add_new_memory at malloc_bf_bm_flb.c:151:22 [opt]
//    148        (my_metadata_t *)mmap_from_system(buffer_size);
//    149    new_metadata->size = buffer_size - sizeof(my_metadata_t);
//    150    new_metadata->next = NULL;
// -> 151    new_metadata->prev = NULL;
//    152    my_add_to_free_list(new_metadata); // 新たに追加された領域をfree_listに追加する
//    153  }
//    154 
// Target 0: (malloc_challenge.bin) stopped.
// warning: malloc_challenge.bin was compiled with optimization - stepping may behave oddly; variables may not be available.