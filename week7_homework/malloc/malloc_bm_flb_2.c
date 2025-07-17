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
  size_t size_and_flag; // 下位ビットをフラグとして使う
  struct my_metadata_t *all_next;
  struct my_metadata_t *all_prev;

  union
  {
    // Freeの時はbinリストのポインタとして使い、allocatedの時はユーザーのデータを書き込む
    struct
    {
      struct my_metadata_t *bin_next;
      struct my_metadata_t *bin_prev;
    } free_pointer;
    char user_payload_start[1];
  } body;

} my_metadata_t;

// ----- ヘルパー関数 -----
static inline void set_size_and_flag(my_metadata_t *meta, size_t size, bool allocated)
{
  meta->size_and_flag = size | (allocated ? 1 : 0);
}

static inline size_t get_size(my_metadata_t *meta)
{
  return meta->size_and_flag & ~7UL; // 下位3ビットを0にしてサイズだけ取り出す
}

static inline bool is_allocated(my_metadata_t *meta)
{
  return (meta->size_and_flag & 1) != 0;
}

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
  my_heap.all_dummy_head.size_and_flag = 0;
  my_heap.all_dummy_head.all_prev = NULL;
  my_heap.all_dummy_head.all_next = &my_heap.all_dummy_tail;
  my_heap.all_dummy_tail.size_and_flag = 0;
  my_heap.all_dummy_tail.all_prev = &my_heap.all_dummy_head;
  my_heap.all_dummy_tail.all_next = NULL;
  my_heap.all_head = &my_heap.all_dummy_head; // free_listの先頭はdummy_headから始まる

  // bin_nextとbin_prevは、all_listのダミーノードでは使用しないのでNULLにしておく
  my_heap.all_dummy_head.body.free_pointer.bin_next = NULL;
  my_heap.all_dummy_head.body.free_pointer.bin_prev = NULL;
  my_heap.all_dummy_tail.body.free_pointer.bin_next = NULL;
  my_heap.all_dummy_tail.body.free_pointer.bin_prev = NULL;

  // binごとのfree_list用
  for (int i = 0; i < NUM_BINS; i++)
  {
    my_heap.bin_dummy_head[i].size_and_flag = 0;
    my_heap.bin_dummy_head[i].body.free_pointer.bin_prev = NULL;
    my_heap.bin_dummy_head[i].body.free_pointer.bin_next = &my_heap.bin_dummy_tail[i];
    my_heap.bin_dummy_tail[i].size_and_flag = 0;
    my_heap.bin_dummy_tail[i].body.free_pointer.bin_prev = &my_heap.bin_dummy_head[i];
    my_heap.bin_dummy_tail[i].body.free_pointer.bin_next = NULL;
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

void my_add_to_bin_list(my_metadata_t *metadata) // binリストにfree_blockを追加, 前に順次追加していく方式
{
  assert(!is_allocated(metadata));                                                        // メモリ領域がfreeである
  assert(!metadata->body.free_pointer.bin_next && !metadata->body.free_pointer.bin_prev); // freeポインタが解放されている

  int bin_index = my_get_bin_index(get_size(metadata)); // サイズから適切なビンを決定
  metadata->body.free_pointer.bin_next = my_heap.bin_head[bin_index]->body.free_pointer.bin_next;
  metadata->body.free_pointer.bin_prev = my_heap.bin_head[bin_index];
  metadata->body.free_pointer.bin_next->body.free_pointer.bin_prev = metadata;
  my_heap.bin_head[bin_index]->body.free_pointer.bin_next = metadata;
}

void my_remove_from_bin_list(my_metadata_t *metadata) // allocatedになった時,mergeされる時に使う
{
  int bin_index = my_get_bin_index(get_size(metadata));                                                     // サイズから適切なビンを決定
  assert(metadata != &my_heap.bin_dummy_head[bin_index] && metadata != &my_heap.bin_dummy_tail[bin_index]); // free_listのdummyでない

  metadata->body.free_pointer.bin_prev->body.free_pointer.bin_next = metadata->body.free_pointer.bin_next; // 前後のノードを繋ぎ直し
  metadata->body.free_pointer.bin_next->body.free_pointer.bin_prev = metadata->body.free_pointer.bin_prev;
  metadata->body.free_pointer.bin_next = NULL; // freeポインタを解放
  metadata->body.free_pointer.bin_prev = NULL;
}

void my_remove_from_all_list(my_metadata_t *metadata) // 基本all_listの要素は削除されないが,mergeでfree_listが結合した時にだけ使う
{
  assert(!is_allocated(metadata));                                  // メモリ領域がfreeである(mergeされる対象である)
  assert(metadata->all_prev != NULL && metadata->all_next != NULL); // all_listのdummyでない

  metadata->all_prev->all_next = metadata->all_next; // 前後のノードを繋ぎ直し
  metadata->all_next->all_prev = metadata->all_prev;
  metadata->all_next = NULL; // allポインタを解放
  metadata->all_prev = NULL;
}

void my_merge_free_block(my_metadata_t *metadata) // current_block（my_freeされたブロック）は、もともとallocatedだったのでbinリストにはいない！
{
  assert(!is_allocated(metadata)); // メモリ領域がfreeである(mergeされる対象である)
  my_metadata_t *current_block = metadata;

  my_metadata_t *next_block = current_block->all_next; // right側のmerge
  size_t current_block_size = get_size(current_block);
  size_t next_block_size = get_size(next_block);
  if (next_block != &my_heap.all_dummy_tail && !is_allocated(next_block))
  {
    my_remove_from_bin_list(next_block); // next_blockをまずbinリストから削除
    my_remove_from_all_list(next_block);
    current_block_size += sizeof(my_metadata_t) + next_block_size; // current_blockとsizeを合算
    set_size_and_flag(current_block, current_block_size, false);   // sizeの情報を更新
  }

  my_metadata_t *prev_block = current_block->all_prev; // left側のmerge
  size_t prev_block_size = get_size(prev_block);
  if (prev_block != &my_heap.all_dummy_head && !is_allocated(prev_block))
  {
    my_remove_from_bin_list(prev_block);                           // prev_blockをまずbinリストから削除
    my_remove_from_all_list(current_block);                        // 基本前に吸収させるのでprevが大きくなる
    prev_block_size += sizeof(my_metadata_t) + current_block_size; // current_blockのsizeを合算し更新
    set_size_and_flag(prev_block, prev_block_size, false);         // sizeの情報を更新
    current_block = prev_block;
  }
  my_add_to_bin_list(current_block); // 最終的な大きさになったブロックを、正しいbinに追加
}

void my_add_to_all_list(my_metadata_t *metadata) // new_memoryを追加する際にアドレス順になるような場所につなげたい時に使う
{
  assert(!metadata->all_next && !metadata->all_prev);
  my_metadata_t *current = &my_heap.all_dummy_head;

  while (current->all_next != &my_heap.all_dummy_tail &&
         (uintptr_t)current->all_next < (uintptr_t)metadata) // metadataのアドレスが current->all_next のアドレスよりも大きくなるまで進める
  {
    current = current->all_next;
  } // このループ後、metadata は current と current->all_next の間に挿入されるべき
  assert(current != metadata);            // アドレスが被っていないことを一応確認
  metadata->all_next = current->all_next; // 前後のノードと繋ぐ
  metadata->all_prev = current;
  current->all_next->all_prev = metadata;
  current->all_next = metadata;
}

void my_add_new_memory()
{
  size_t buffer_size = 4096;
  my_metadata_t *new_metadata = (my_metadata_t *)mmap_from_system(buffer_size);
  size_t size = buffer_size - sizeof(my_metadata_t);
  set_size_and_flag(new_metadata, size, false); // size,flagの情報を追加する
  new_metadata->all_next = NULL;
  new_metadata->all_prev = NULL;
  new_metadata->body.free_pointer.bin_next = NULL;
  new_metadata->body.free_pointer.bin_prev = NULL;
  my_add_to_all_list(new_metadata); // 新たに追加された領域をall_listに追加する
  my_add_to_bin_list(new_metadata); // 新たに追加された領域をfree_listに追加する
}

/* Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!) */

void *my_malloc(size_t size)
{
  my_metadata_t *best_fit_metadata = NULL;

  // bestfit
  // for (int bin_index = my_get_bin_index(size); bin_index < NUM_BINS; bin_index++) // 要求されたサイズのbinから、最後まで順番にすべて探す
  // {
  //   my_metadata_t *metadata = my_heap.bin_head[bin_index]->body.free_pointer.bin_next;
  //   while (metadata != &my_heap.bin_dummy_tail[bin_index])
  //   {
  //     if (get_size(metadata) >= size)
  //     {
  //       if (best_fit_metadata == NULL || get_size(metadata) < get_size(best_fit_metadata)) // 今まで見つけたbest_fitよりサイズが小さければより良い候補
  //       {
  //         best_fit_metadata = metadata;
  //       }
  //     }
  //     metadata = metadata->body.free_pointer.bin_next;
  //   }
  // }

  // First fit
  for (int bin_index = my_get_bin_index(size); bin_index < NUM_BINS; bin_index++)
  {
    my_metadata_t *metadata = my_heap.bin_head[bin_index]->body.free_pointer.bin_next;
    while (metadata != &my_heap.bin_dummy_tail[bin_index])
    {
      if (get_size(metadata) >= size)
      {
        // ここでは最初に見つかったものを採用するシンプルな形にする
        best_fit_metadata = metadata;
        goto found; // 見つかったらループを抜ける
      }
      metadata = metadata->body.free_pointer.bin_next;
    }
  }
found:; // ループを抜けるためのラベル

  if (!best_fit_metadata) // 最適な空きスロットが見つからなかった場合
  {
    my_add_new_memory();
    return my_malloc(size); // 再帰で呼び出し
  }

  // メモリの割り当て
  my_metadata_t *metadata = best_fit_metadata; // ptr(割り当てる領域の開始アドレス)はmetadataの次のアドレス
  my_remove_from_bin_list(metadata);
  void *ptr = metadata + 1;
  set_size_and_flag(metadata, get_size(metadata), true); // flagのみ変化させる
  size_t remaining_size = get_size(metadata) - size;
  if (remaining_size > sizeof(my_metadata_t)) // my_metadata_tが入る大きさ分の残りサイズがある場合のみ、残りをfree_listに繋げる
  {
    set_size_and_flag(metadata, size, true); // size,flagの情報を追加する
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    size_t new_metadata_size = remaining_size - sizeof(my_metadata_t);
    set_size_and_flag(new_metadata, new_metadata_size, false); // size,flagの情報を追加する
    new_metadata->body.free_pointer.bin_next = NULL;           // binポインタを解放しておく
    new_metadata->body.free_pointer.bin_prev = NULL;

    new_metadata->all_next = metadata->all_next; // アドレス順に探すのではなく前後繋ぎ直す
    new_metadata->all_prev = metadata;
    metadata->all_next->all_prev = new_metadata;
    metadata->all_next = new_metadata;
    my_add_to_bin_list(new_metadata); // 新たにできた領域をfree_listに追加する
  }
  return ptr; // ptr(割り当てる領域の開始アドレス)を返す
}

void my_free(void *ptr)
{
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  if (!is_allocated(metadata)) // すでにfreeだったら何もしない
  {
    fprintf(stderr, "Error: Double free detected for pointer %p\n", ptr);
    return;
  }
  metadata->body.free_pointer.bin_next = NULL;
  metadata->body.free_pointer.bin_prev = NULL;
  set_size_and_flag(metadata, get_size(metadata), false); // size,flagの情報を更新する
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

// RESULT (Best fit)
// ====================================================
// Challenge #1    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|               7 =>             274
// Utilization [%] |              70 =>              60
// ====================================================
// Challenge #2    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|               5 =>             219
// Utilization [%] |              40 =>              22
// ====================================================
// Challenge #3    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|              94 =>             180
// Utilization [%] |               9 =>              33
// ====================================================
// Challenge #4    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|           22839 =>             167
// Utilization [%] |              15 =>              75
// ====================================================
// Challenge #5    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|           14125 =>             152
// Utilization [%] |              15 =>              76

// Challenge done!
// Please copy & paste the following data in the score sheet!
// 274,60,219,22,180,33,167,75,152,76,

// RESULT(First fit)
// ====================================================
// Challenge #1    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|               8 =>              14
// Utilization [%] |              70 =>              60
// ====================================================
// Challenge #2    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|               4 =>               7
// Utilization [%] |              40 =>              22
// ====================================================
// Challenge #3    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|              88 =>              11
// Utilization [%] |               9 =>              33
// ====================================================
// Challenge #4    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|           23875 =>              88
// Utilization [%] |              15 =>              73
// ====================================================
// Challenge #5    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|           17197 =>              61
// Utilization [%] |              15 =>              74

// Challenge done!
// Please copy & paste the following data in the score sheet!
// 14,60,7,22,11,33,88,73,61,74,