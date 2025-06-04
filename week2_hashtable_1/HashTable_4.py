# This file is 3rd ver.

# *** Progress ***
# Please check this function. 
# Adjust bucket size
# search nearest prime number

# *** what is the changes? ***
# hash function: sum just ASCII code -(ver.2)-> add by incrementary shifting place value and sum up 
# bucket_size: not chnged. 
#              always fixed. size < 100 or used bucket >= 30%.

# *** Plan ***
# If the hash table works with mostly O(1), the execution time of each iteration should not depend on the number of items in the hash table. To achieve this
# 1) implement rehashing (Hint: expand / shrink the hash table when the number of items in the hash table hits some threshold) 
# 2) tweak the hash function (Hint: think about ways to reduce hash conflicts).
import random, sys, time

# *** Hash function ***
# |key|: string
# Return /value/: a hash value
# add by incrementary shifting place value and sum up
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
    def __init__(self, key, value, next_item):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next_item


# *** The main data structure of the hash table ***
# stores key - value pairs.
# Note: The key must be a string. The value can be any type.
class HashTable:

    # *** Initialize the hash table. ***
    # self.bucket_size: The bucket size.
    # self.buckets: An array of the buckets. self.buckets[hash % self.bucket_size]
    #                 stores a linked list of items whose hash value is |hash|.
    # self.item_count: The total number of items in the hash table.
    def __init__(self,initial_bucket_size=97):
        # Note: Use prime number for bucket_size to reduce hash conflicts.
        # Note: rehash to fit data size
        self.bucket_size = initial_bucket_size
        self.buckets = [None] * self.bucket_size
        self.item_count = 0
        self.rehashing = False 

    # *** Put an item to the hash table. ***
    # |key|: The key of the item.
    # |value|: The value of the item.
    # Return /bool/: True if a new item is added. 
    #                False if the key already exists and the value is updated.
    # Note: If the key already exists, the corresponding value is updated to a new value.
    def put(self, key, value):
        assert type(key) == str
        # Change: delete assert.
        # |bucket_index|: hash value % bucket_size
        if not self.rehashing:
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
            self.adjust_size()
            return True
        else:
            bucket_index = calculate_hash(key) % self.bucket_size
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
        # Change: delete assert.
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
        # Change: delete assert.
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
    
    # *** Adjust bucket size ***
    # 1) Use prime number.
    # 2) Expand to twice if used bucket size >= 70%.
    # 3) Shrink to half if used bucket size <= 30%.
    # Note: Use PrimeSearch function.
    # usage_rate: total number of items(item_count) / now bucket size(bucket_size) 
    # Return /value/: adjusted new_size.
    def adjust_size(self):
        usage_rate = self.item_count/self.bucket_size
        new_size = self.bucket_size
        if usage_rate <= 0.3:
            new_size = self.find_prime(int(self.bucket_size*0.5))
        elif usage_rate >= 0.7:
            new_size = self.find_prime(int(self.bucket_size*2))
        if new_size != self.bucket_size:
            self.rehash(new_size)
    
    # *** Rehash function ***
    # |new_size|: adjusted new bucket size.
    # Rehash elements in each original bucket to fit new size.
    def rehash(self,new_size):
        self.rehashing = True
        old_buckets = self.buckets
        self.bucket_size = new_size
        self.buckets = [None]*(self.bucket_size)
        self.item_count = 0
        for bucket in old_buckets:
            item = bucket
            while item:
                self.put(item.key,item.value)
                item = item.next
        self.rehashing = False

    # *** search nearest prime number ***
    # FindPrime(number): search prime number >= adjusted bucket_size.
    # MillerRabin(n,k=5): primality test to judge prime number or not.
    def find_prime(self,number):
        if number <= 2:
            return 2
        # adjust if number is not odd.
        if number % 2 == 0:
            n = number+1
        else:
            n = number
        # return n if MillerRabin == True
        while True:
            if self.miller_rabin(n,k=5):
                return n
            else:
                n += 2
    
    def miller_rabin(self,n,k=5):
        # exclude non-prime numbers.
        if n == 1:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        # find d and s. (n-1 = 2^s * d)
        d = n-1
        s = 0
        while d%2 == 0:
            d //= 2
            s += 1
        # Run the test k times.
        for _ in range(k):
            # Question: Why doesn't need "random.seed(n)"??
            # Question: (2,n-1) is 2 <= random <= n-1 ??
            a = random.randint(2,n-1)
            x = pow(a,d,n)
            if x == 1 or x == n-1:
                continue
            maybe_prime = False
            for _ in range(s-1):
                x = pow(x,2,n)
                if x == n-1:
                    maybe_prime = True
                    break
                if x == 1:
                    return False
            if not maybe_prime:
                return False
        return True

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
    print(f"Size: {hash_table.size()}")

    for iteration in range(100):
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.delete(str(rand))
    
    if hash_table.size() != 0:
        print(f"Error: Hash table not empty. Size: {hash_table.size()}")

    assert hash_table.size() == 0
    print("Performance tests passed!")


if __name__ == "__main__":
    functional_test()
    performance_test()

