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
} my_metadata_t;

typedef struct my_heap_t
{
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

void my_add_to_free_list(my_metadata_t *metadata)
{
  assert(!metadata->next);
  metadata->next = my_heap.free_head;
  my_heap.free_head = metadata;
}

void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev)
{
  if (prev)
  {
    prev->next = metadata->next;
  }
  else
  {
    my_heap.free_head = metadata->next;
  }
  metadata->next = NULL;
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize()
{
  my_heap.free_head = &my_heap.dummy;
  my_heap.dummy.size = 0;
  my_heap.dummy.next = NULL;
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
void *my_malloc(size_t size)
{
  my_metadata_t *metadata = my_heap.free_head;
  my_metadata_t *prev = NULL;

  // Worst-fit: Find the largest free slot that fits the object.
  my_metadata_t *worst_fit_metadata = NULL;
  my_metadata_t *worst_fit_prev = NULL;
  size_t max_size = 0; // 最大のサイズを追跡するため、0で初期化

  // フリーリスト全体を走査
  while (metadata)
  {
    if (metadata->size >= size)
    { // 要求されたサイズを満たすブロックか？
      if (metadata->size > max_size)
      { // より大きいブロックか？
        max_size = metadata->size;
        worst_fit_metadata = metadata;
        worst_fit_prev = prev;
      }
    }
    prev = metadata;           // prev を更新
    metadata = metadata->next; // 次の要素へ
  }

  // ループ後、worst_fit_metadata がワーストフィットのブロックを指しているはず
  metadata = worst_fit_metadata;
  prev = worst_fit_prev;

  if (!metadata)
  {
    // There was no free slot available. Request new memory.
    // ... (この部分は変更なし) ...
    size_t buffer_size = 4096;
    my_metadata_t *new_metadata =
        (my_metadata_t *)mmap_from_system(buffer_size); // 変数名衝突を避けるためnew_metadataに
    new_metadata->size = buffer_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    my_add_to_free_list(new_metadata);
    return my_malloc(size); // 再帰呼び出し
  }

  // ... (以降のコードは変更なし) ...
  void *ptr = metadata + 1;
  size_t remaining_size = metadata->size - size;
  my_remove_from_free_list(metadata, prev); 
  if (remaining_size > sizeof(my_metadata_t))
  {
    metadata->size = size;
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
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
  // Add the free slot to the free list.
  my_add_to_free_list(metadata);
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


//RESULT
// ====================================================
// Challenge #1    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|              12 =>            1582
// Utilization [%] |              70 =>              70
// ====================================================
// Challenge #2    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|               7 =>            1166
// Utilization [%] |              40 =>              40
// ====================================================
// Challenge #3    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|             130 =>           68286
// Utilization [%] |               9 =>               4
// ====================================================
// Challenge #4    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|           23535 =>          849108
// Utilization [%] |              15 =>               7
// ====================================================
// Challenge #5    |   simple_malloc =>       my_malloc
// --------------- + --------------- => ---------------
//        Time [ms]|           15738 =>          705569
// Utilization [%] |              15 =>               7

// Challenge done!
// Please copy & paste the following data in the score sheet!
// 1582,70,1166,40,68286,4,849108,7,705569,7,