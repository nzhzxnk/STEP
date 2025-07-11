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

typedef struct my_metadata_t {
  size_t size;
  struct my_metadata_t *next;
} my_metadata_t;

typedef struct my_heap_t {
  my_metadata_t *free_head;
  my_metadata_t dummy;
} my_heap_t;

//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//
my_heap_t my_heap;

//
// Helper functions (feel free to add/remove/edit!)
//

void my_add_to_free_list(my_metadata_t *metadata) {
  assert(!metadata->next);
  metadata->next = my_heap.free_head;
  my_heap.free_head = metadata;
}

void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev) {
  if (prev) {
    prev->next = metadata->next;
  } else {
    my_heap.free_head = metadata->next;
  }
  metadata->next = NULL;
}

void my_add_new_memory()
{
  size_t buffer_size = 4096;
  my_metadata_t *new_metadata =
      (my_metadata_t *)mmap_from_system(buffer_size);
  new_metadata->size = buffer_size - sizeof(my_metadata_t);
  new_metadata->next = NULL;
  my_add_to_free_list(new_metadata); // 新たに追加された領域をfree_listに追加する
}


void my_initialize() {
  my_heap.free_head = &my_heap.dummy;
  my_heap.dummy.size = 0;
  my_heap.dummy.next = NULL;
}


//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

void *my_malloc(size_t size) {
  my_metadata_t *metadata = my_heap.free_head;
  my_metadata_t *prev = NULL;
  // First-fit: Find the first free slot the object fits.
  // TODO: Update this logic to Best-fit!
  while (metadata && metadata->size < size) {
    prev = metadata;
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
  my_remove_from_free_list(metadata, prev);

  if (remaining_size > sizeof(my_metadata_t)) {
    metadata->size = size;
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    // Add the remaining free slot to the free list.
    my_add_to_free_list(new_metadata);
  }
  return ptr;
}

void my_free(void *ptr) {
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  my_metadata_t *next_metadata = metadata->next;
  // free_listを辿ったnext_metadataのアドレスと、metadataのfree_blockの次のブロックのアドレスが一致していれば、次もfree_blockが連続していることになる。
  if (next_metadata == (my_metadata_t *)((char *)metadata + sizeof(my_metadata_t) + metadata->size)){
    my_remove_from_free_list(next_metadata, metadata); // next_metadataをフリーリストから削除し、free_listを繋ぎ直す
    metadata->size += sizeof(my_metadata_t) + next_metadata->size; // 解放ブロックのサイズを、隣の空きブロックのサイズとメタデータ分だけ増やす
    }
  my_add_to_free_list(metadata);
}

// This is called at the end of each challenge.
void my_finalize() {
  // Nothing is here for now.
  // feel free to add something if you want!
}

void test() {
  // Implement here!
  assert(1 == 1); /* 1 is 1. That's always true! (You can remove this.) */
}

// RESULT
// ====================================================
// Challenge #1    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|              13 =>              11
// Utilization [%] |              70 =>              70
// ====================================================
// Challenge #2    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|              10 =>               7
// Utilization [%] |              40 =>              40
// ====================================================
// Challenge #3    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|             140 =>             136
// Utilization [%] |               9 =>               9
// ====================================================
// Challenge #4    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|           24032 =>           24371
// Utilization [%] |              15 =>              15
// ====================================================
// Challenge #5    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|           16061 =>           17226
// Utilization [%] |              15 =>              15

// Challenge done!
// Please copy & paste the following data in the score sheet!
// 11,70,7,40,136,9,24371,15,17226,15,