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
# 0 0.211110
# 1 0.389402
# 2 0.561643
# 3 0.736007
# 4 0.916840
# 5 1.111591
# 6 1.338951
# 7 1.585719
# 8 1.963091
# 9 2.480982
# 10 3.373154
# 11 4.272315
# 12 5.519355
# 13 6.831632
# 14 8.323012
# 15 9.852235
# 16 10.718235
# 17 12.756111
# 18 13.386770
# 19 15.524495
# 20 16.761326
# 21 17.293571
# 22 19.308010
# 23 20.720812
# 24 21.796502
# 25 22.815721
# 26 20.892565
# 27 25.502285
# 28 26.338030
# 29 26.937291
# 30 24.888432
# 31 30.844483
# 32 31.269241
# 33 28.836388
# 34 33.978998
# 35 30.592239
# 36 32.614169
# 37 37.000189
# 38 35.835199
# 39 35.268525
# 40 41.213141
# 41 33.071392
# 42 35.186871
# 43 42.560300
# 44 43.128719
# 45 47.416870
# 46 47.014186
# 47 48.586890
# 48 50.633027
# 49 46.672540
# 50 52.083964
# 51 53.847056
# 52 55.152806
# 53 56.193474
# 54 56.561371
# 55 57.640527
# 56 58.146392
# 57 60.442144
# 58 56.654197
# 59 63.689257
# 60 64.023534
# 61 64.685300
# 62 66.424904
# 63 68.323913
# 64 68.966904
# 65 70.871026
# 66 72.148128
# 67 72.464606
# 68 72.332983
# 69 75.237828
# 70 70.991077
# 71 77.847962
# 72 77.251363
# 73 77.653672
# 74 80.431994
# 75 81.282175
# 76 83.108947
# 77 85.137648
# 78 85.268104
# 79 83.494623
# 80 84.661698
# 81 87.356591
# 82 89.719527
# 83 90.597769
# 84 92.083813
# 85 93.448718
# 86 94.012827
# 87 93.067492
# 88 95.697894
# 89 98.165303
# 90 98.075584
# 91 99.143306
# 92 99.974025
# 93 100.926465
# 94 103.099114
# 95 101.214981
# 96 103.090706
# 97 106.706911
# 98 108.875614
# 99 107.363010
# Question: Why did it take longer when PC sleeping?? 
# Question: Why didn't show "Performance tests passed!"??

if __name__ == "__main__":
    functional_test()
    performance_test()

