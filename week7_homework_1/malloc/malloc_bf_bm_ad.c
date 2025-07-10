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
  my_metadata_t *free_head;
  my_metadata_t dummy_head; // リストの先頭のダミーノード
  my_metadata_t dummy_tail; // リストの末尾のダミーノード
} my_heap_t;

//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//
my_heap_t my_heap;

//
// Helper functions (feel free to add/remove/edit!)
//

void my_remove_from_free_list(my_metadata_t *metadata)
{ // ダミーノードは削除しない
  assert(metadata != &my_heap.dummy_head);
  assert(metadata != &my_heap.dummy_tail);
  // prevとnext同士を繋ぐ
  metadata->prev->next = metadata->next;
  metadata->next->prev = metadata->prev;
  metadata->next = NULL; // 削除されたノードのポインタをクリア
  metadata->prev = NULL; // 削除されたノードのポインタをクリア
}

void my_merge_free_list(my_metadata_t *metadata)
{
  // free_listを辿ったnext_metadataのアドレスと、metadataのfree_blockの次のブロックのアドレスが一致していれば、次もfree_blockが連続していることになる。
  if (metadata->prev != &my_heap.dummy_head && metadata->prev != &my_heap.dummy_head)
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
    }
  }
}

void my_add_to_free_list(my_metadata_t *metadata) // アドレス順に連結リストを保存
{
  assert(!metadata->next && !metadata->prev); // free_listでなければエラー
  // アドレス順に挿入位置を探す
  my_metadata_t *current = my_heap.free_head->next; // ダミーヘッドから開始
  // metadataのアドレスがcurrentのアドレスよりも大きくなるまで進む
  // currentはmetadataの物理的な前、または挿入位置になるはずのノード
  if (current == &my_heap.dummy_tail || (uintptr_t)metadata < (uintptr_t)current)
  {
    metadata->next = my_heap.free_head->next;
    metadata->prev = my_heap.free_head;
    metadata->next->prev = metadata;
    my_heap.free_head->next = metadata;
  }
  else
  {
    while (current->next != &my_heap.dummy_tail && (uintptr_t)current < (uintptr_t)metadata)
    {
      current = current->next;
    }
    // (uintptr_t)current < (uintptr_t)metadata <= (uintptr_t)current->nextとなるはずなので、metadataは間に入る
    metadata->next = current->next;
    metadata->prev = current;
    metadata->next->prev = metadata;
    current->next = metadata;
  }
}

void my_add_new_memory()
{
  size_t buffer_size = 4096;
  my_metadata_t *new_metadata = (my_metadata_t *)mmap_from_system(buffer_size);
  new_metadata->size = buffer_size - sizeof(my_metadata_t);
  new_metadata->next = NULL;
  new_metadata->prev = NULL;
  my_add_to_free_list(new_metadata); // 新たに追加された領域をfree_listに追加する
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize()
{
  my_heap.dummy_head.size = 0;
  my_heap.dummy_head.prev = NULL;
  my_heap.dummy_head.next = &my_heap.dummy_tail;

  my_heap.dummy_tail.size = 0;
  my_heap.dummy_tail.prev = &my_heap.dummy_head;
  my_heap.dummy_tail.next = NULL;

  my_heap.free_head = &my_heap.dummy_head; // free_listの先頭はdummy_headから始まる
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
void *my_malloc(size_t size)
{
  // metadata配列(free_list)の先頭と、その直前のポインタを設定
  my_metadata_t *metadata = my_heap.free_head; // metadata配列の先頭ポインタ

  // Best-fit: Find the smallest free slot that fits the object.
  my_metadata_t *best_fit_metadata = NULL; // 最適なfree_blockのmetadataを指すポインタ
  size_t min_diff = (size_t)-1;            // size_t(符号なし整数型)が取れる最大値で初期化。
  // モジュロ演算（剰余演算）で-1は全てのビットが1であると表現されるので最大値になる。

  while (metadata) // metadata配列の最後まで走査
  {
    if (metadata->size >= size)
    { // 要求されたsizeを満たすブロックである場合
      size_t current_diff = metadata->size - size;
      if (current_diff < min_diff)
      { // かつ現時点でのfree_blockの最小値より小さい場合、best_fit_metadata, best_fit_prev, min_diffを更新
        best_fit_metadata = metadata;
        min_diff = current_diff;
      }
    }
    metadata = metadata->next; // metadataを次の要素へ更新
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
  void *ptr = metadata + 1;                      // ptr(割り当てる領域の開始アドレス)はmetadataの次のアドレス
  size_t remaining_size = metadata->size - size; // 割り当て後の残りサイズを計算
  my_remove_from_free_list(metadata);            // メモリを割り当て、その領域をfree_listから削除
  if (remaining_size > sizeof(my_metadata_t))    // my_metadata_tが入る大きさ分の残りサイズがある場合のみ、残りをfree_listに繋げる
  {
    metadata->size = size;
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
  my_merge_free_list(metadata);
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
// ====================================================
// Challenge #1    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|              11 =>            1713
// Utilization [%] |              70 =>              65
// ====================================================
// Challenge #2    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|               7 =>            1111
// Utilization [%] |              40 =>              31
// ====================================================
// Challenge #3    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|             128 =>            1050
// Utilization [%] |               9 =>              44
// ====================================================
// Challenge #4    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|           13943 =>            8310
// Utilization [%] |              15 =>              73
// ====================================================
// Challenge #5    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|            8812 =>            4656
// Utilization [%] |              15 =>              76

// Challenge done!
// Please copy & paste the following data in the score sheet!
// 1713,65,1111,31,1050,44,8310,73,4656,76,