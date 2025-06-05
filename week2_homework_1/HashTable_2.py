# This file is 2nd ver.

# *** what is the changes? ***
# hash function: sum just ASCII code --> add by incrementary shifting place value and sum up
# bucket_size: not changed. 
#              always fixed. size < 100 or used bucket >= 30%.

import random, sys, time

# *** Hash function ***
# |key|: string
# Return /value/: a hash value
# New: hash += ord(i)*(10**i)
#      add by incrementary shifting place value and sum up
def calculate_hash(key):
    assert type(key) == str
    hash_val = 0
    for char in key:
        hash_val += hash_val * 31 + ord(char)
    return hash_val


# *** An item object ***
# represents one key - value pair in the hash table. 
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
        for i in range(100000):
            rand = random.randint(0, 100000000)
            hash_table.get(str(rand))
        end = time.time()
        print("%d %.6f" % (iteration, end - begin))
    # print(f"Size: {hash_table.size()}")

    for iteration in range(100):
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.delete(str(rand))

    assert hash_table.size() == 0
    print("Performance tests passed!")

# *** Test result ***
# a little faster than ver.1 
# Functional tests passed!
# 0 0.103029
# 1 0.167331
# 2 0.226468
# 3 0.290443
# 4 0.451170
# 5 0.439451
# 6 0.591323
# 7 0.746730
# 8 0.784426
# 9 1.071424
# 10 1.408922
# 11 1.911684
# 12 2.352183
# 13 2.692618
# 14 3.257649
# 15 3.938788
# 16 4.395614
# 17 4.903342
# 18 4.908935
# 19 5.790589
# 20 6.043435
# 21 6.583637
# 22 7.042440
# 23 7.508603
# 24 8.016069
# 25 8.382018
# 26 9.005651
# 27 9.460289
# 28 9.264766
# 29 7.925213
# 30 5.760906
# 31 7.336508
# 32 11.563026
# 33 8.058742
# 34 12.319257
# 35 8.595804
# 36 11.539530
# 37 14.226369
# 38 14.745250
# 39 14.966057
# 40 15.436457
# 41 10.259016
# 42 8.372497
# 43 12.263175
# 44 10.391977
# 45 16.075582
# 46 10.301089
# 47 9.603241
# 48 10.519098
# 49 16.649464
# 50 19.510510
# 51 19.470840
# 52 19.261433
# 53 13.744855

if __name__ == "__main__":
    functional_test()
    performance_test()

