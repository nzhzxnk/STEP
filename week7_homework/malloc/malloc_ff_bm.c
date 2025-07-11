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

void my_add_to_free_list(my_metadata_t *metadata)
{
  assert(!metadata->next && !metadata->prev);
  metadata->next = my_heap.free_head->next;
  metadata->prev = my_heap.free_head;
  metadata->next->prev = metadata;
  my_heap.free_head->next = metadata;
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
// First-fit: Find the first free slot the object fits.
  // TODO: Update this logic to Best-fit!
  while (metadata && metadata->size < size) {
    metadata = metadata->next;
  }

  if (!metadata) {
    size_t buffer_size = 4096;
    my_metadata_t *metadata = (my_metadata_t *)mmap_from_system(buffer_size);
    metadata->size = buffer_size - sizeof(my_metadata_t);
    metadata->next = NULL;
    // Add the memory region to the free list.
    my_add_to_free_list(metadata);
    // Now, try my_malloc() again. This should succeed.
    return my_malloc(size);
  }
  void *ptr = metadata + 1;
  size_t remaining_size = metadata->size - size;
  // Remove the free slot from the free list.
  my_remove_from_free_list(metadata);

  if (remaining_size > sizeof(my_metadata_t)) {
    metadata->size = size;
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    new_metadata->prev = NULL;
    // Add the remaining free slot to the free list.
    my_add_to_free_list(new_metadata);
  }
  return ptr;
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
//        Time [ms]|              11 =>               9
// Utilization [%] |              70 =>              65
// ====================================================
// Challenge #2    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|               7 =>               9
// Utilization [%] |              40 =>              31
// ====================================================
// Challenge #3    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|             133 =>             123
// Utilization [%] |               9 =>               8
// ====================================================
// Challenge #4    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|           28496 =>           27079
// Utilization [%] |              15 =>              15
// ====================================================
// Challenge #5    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|           19787 =>           19152
// Utilization [%] |              15 =>              15

// Challenge done!
// Please copy & paste the following data in the score sheet!
// 9,65,9,31,123,8,27079,15,19152,15,