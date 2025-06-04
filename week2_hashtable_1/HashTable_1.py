# This file is 1st ver.
# hash function: the sum of ASCII code.
# bucket_size: always fixed. size < 100 or used bucket >= 30%.

import random, sys, time

# *** Hash function ***
# |key|: string
# Return /value/: a hash value
# Note: This is not a good hash function. 
def calculate_hash(key):
    assert type(key) == str
    hash = 0
    for i in key:
        hash += ord(i)
    return hash


# *** An item object ***
# represents one key - value pair in the hash table. ***
class Item:
    # |key|: The key of the item. The key must be a string.
    # |value|: The value of the item. The value can be any type.
    # |next|: The next item in the linked list. If this is the last item in the
    #         linked list, |next| is None.
    # Question: what is __init__ ??
    def __init__(self, key, value, next):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next


# *** The main data structure of the hash table ***
# stores key - value pairs.
# Note: The key must be a string. The value can be any type.
class HashTable:
    # *** Initialize the hash table. ***
    # |self.bucket_size|: The bucket size.
    # |self.buckets|: An array of the buckets. self.buckets[hash % self.bucket_size]
    #                 stores a linked list of items whose hash value is |hash|.
    # |self.item_count|: The total number of items in the hash table.
    def __init__(self):
        # Note: Use prime number for bucket_size to reduce hash conflicts.
        # Note: rehash to fit data size
        self.bucket_size = 97
        self.buckets = [None] * self.bucket_size
        self.item_count = 0

    # *** Put an item to the hash table. ***
    # |key|: The key of the item.
    # |value|: The value of the item.
    # Return /bool/: True if a new item is added. 
    #                False if the key already exists and the value is updated.
    # Note: If the key already exists, the corresponding value is updated to a new value.
    def put(self, key, value):
        assert type(key) == str
        # Question: Why is there this code ??
        self.check_size() 
        # |bucket_index|: hash value % bucket_size
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                item.value = value
                return False
            item = item.next
        # Note: new item is class Item.
        #       the type of |buckets[bucket_index]| and |item| and |new_item| is lincked-list.
        new_item = Item(key, value, self.buckets[bucket_index])
        self.buckets[bucket_index] = new_item
        self.item_count += 1
        return True

    # *** Get an item from the hash table. ***
    # |key|: The key.
    # Return /(value, bool)/: If the item is found, (the value of the item, True) is returned.
    #                         Otherwise, (None, False) is returned.
    def get(self, key):
        assert type(key) == str
        # Note: Don't remove this code.
        self.check_size() 
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                return (item.value, True)
            item = item.next
        return (None, False)

    # *** Delete an item from the hash table. ***
    # |key|: The key.
    # Return /bool/: True if the item is found and deleted successfully.
    #                False otherwise.
    def delete(self, key):
        assert type(key) == str
        # Note: Don't remove this code.
        self.check_size() 
        bucket_index = calculate_hash(key) % self.bucket_size
        cur_item = self.buckets[bucket_index]
        prv_item = None
        while cur_item:
            if cur_item.key == key:
                if prv_item:
                    prv_item.next = cur_item.next
                else:
                    self.buckets[bucket_index] = cur_item.next
                self.item_count -= 1
                return True
            prv_item = cur_item
            cur_item = cur_item.next
        return False

    # *** Return the total number of items in the hash table. ***
    def size(self):
        return self.item_count

    # *** Check reasonable bucket size. ***
    # Note: Define the base of "reasonable" 
    # Note: now base of "reasonable"
    #       (The bucket size < 100 or the used buckets >= 30%) == True
    # Tips: assert function is to continue if True
    #                          to show "Assertation error" if False
    # Question: Why "Don't change this function." ??
    def check_size(self):
        assert (self.bucket_size < 100 or
                self.item_count >= self.bucket_size * 0.3)


# *** Test the functional behavior of the hash table. ***
def functional_test():
    hash_table = HashTable()

    assert hash_table.put("aaa", 1) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.size() == 1

    assert hash_table.put("bbb", 2) == True
    assert hash_table.put("ccc", 3) == True
    assert hash_table.put("ddd", 4) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.get("bbb") == (2, True)
    assert hash_table.get("ccc") == (3, True)
    assert hash_table.get("ddd") == (4, True)
    assert hash_table.get("a") == (None, False)
    assert hash_table.get("aa") == (None, False)
    assert hash_table.get("aaaa") == (None, False)
    assert hash_table.size() == 4

    assert hash_table.put("aaa", 11) == False
    assert hash_table.get("aaa") == (11, True)
    assert hash_table.size() == 4

    assert hash_table.delete("aaa") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.size() == 3

    assert hash_table.delete("a") == False
    assert hash_table.delete("aa") == False
    assert hash_table.delete("aaa") == False
    assert hash_table.delete("aaaa") == False

    assert hash_table.delete("ddd") == True
    assert hash_table.delete("ccc") == True
    assert hash_table.delete("bbb") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.get("bbb") == (None, False)
    assert hash_table.get("ccc") == (None, False)
    assert hash_table.get("ddd") == (None, False)
    assert hash_table.size() == 0

    assert hash_table.put("abc", 1) == True
    assert hash_table.put("acb", 2) == True
    assert hash_table.put("bac", 3) == True
    assert hash_table.put("bca", 4) == True
    assert hash_table.put("cab", 5) == True
    assert hash_table.put("cba", 6) == True
    assert hash_table.get("abc") == (1, True)
    assert hash_table.get("acb") == (2, True)
    assert hash_table.get("bac") == (3, True)
    assert hash_table.get("bca") == (4, True)
    assert hash_table.get("cab") == (5, True)
    assert hash_table.get("cba") == (6, True)
    assert hash_table.size() == 6

    assert hash_table.delete("abc") == True
    assert hash_table.delete("cba") == True
    assert hash_table.delete("bac") == True
    assert hash_table.delete("bca") == True
    assert hash_table.delete("acb") == True
    assert hash_table.delete("cab") == True
    assert hash_table.size() == 0
    print("Functional tests passed!")


# *** Test the performance of the hash table. ***
# add elements in increments of 10,000.
# measure the time for each increments.

def performance_test():
    hash_table = HashTable()

    for iteration in range(100):
        begin = time.time()
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.put(str(rand), str(rand))
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.get(str(rand))
        end = time.time()
        print("%d %.6f" % (iteration, end - begin))

    for iteration in range(100):
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.delete(str(rand))

    assert hash_table.size() == 0
    print("Performance tests passed!")

# *** Test result ***
# Functional tests passed!
# 0 0.210832
# 1 0.387767
# 2 0.554324
# 3 0.732879
# 4 0.905024
# 5 1.111298
# 6 1.351224
# 7 1.618842
# 8 1.996607
# 9 2.470028
# 10 3.408493
# 11 4.411258
# 12 5.618850
# 13 6.721188
# 14 8.227301
# 15 9.683473
# 16 11.002922
# 17 12.748903
# 18 13.706522
# 19 13.536983
# 20 16.577821
# 21 17.582235
# 22 19.176073
# 23 20.635081
# 24 21.830416
# 25 22.573998
# 26 132.025066
# 27 25.709592
# 28 26.812965
# 29 28.329325
# 30 29.387542
# 31 36.499623
# 32 28.057518
# 33 32.165396
# 34 33.935676
# 35 33.190548
# 36 36.661433
# 37 37.614051
# 38 38.679227
# 39 81.966926
# 40 41.298079
# 41 42.577914
# 42 119.516741
# 43 42.655251
# 44 45.661506
# 45 44.971328
# 46 47.896352
# 47 48.032892
# 48 50.953002
# 49 50.112490
# 50 52.865298
# 51 54.351479
# 52 55.437771
# 53 56.193474
# 54 56.259193
# 55 57.375705
# 56 58.230155
# 57 60.480125
# 58 61.004376
# 59 61.258848
# 60 64.967077
# 61 65.238326
# 62 67.205724
# 63 67.940463
# 64 69.708317
# 65 155.034805
# 66 72.238394
# 67 264.725355
# 68 359.172206
# 69 74.957002
# 70 95.132399
# 71 78.181520
# 72 77.251363
# 73 77.653672
# 74 80.431994
# 75 147.282175
# 76 83.108947
# 77 140.137648
# 78 85.268104
# 79 113.494623
# 80 84.661698
# 81 87.356591
# 82 89.719527
# 83 280.597769
# 84 92.083813
# 85 93.448718
# 86 94.012827
# 87 193.067492
# 88 95.697894
# 89 98.165303
# 90 98.075584
# 91 204.143306
# 92 99.974025
# 93 100.926465
# 94 103.099114
# 95 151.214981
# 96 113.090706
# 97 106.706911
# 98 108.875614
# 99 107.363010
# Question: Why did it take longer when PC sleeping?? 
# Question: Why didn't show "Performance tests passed!"??

if __name__ == "__main__":
    functional_test()
    performance_test()

