# *** progress ***
# 25/06/05 21:20 edit comment now

# *** Summary ***
# hash function: add by incrementary shifting place value and sum up. 
# bucket_size: Adjust bucket size to fit item count.
# 1) Use prime number.
# 2) Expand to twice if used bucket size >= 70%.
# 3) Shrink to half if used bucket size <= 30%.
# Node: Doubly linked list.

# *** Plan ***
# Design a cache that achieves the following operations with mostly O(1)
# Implement a data structure that stores the most recently accessed N pages.
# 1) When a pair of <URL, Web page> is given, find if the given pair is contained in the cache or not
# 2) If the pair is not found, insert the pair into the cache after evicting the least recently accessed pair

import sys,random,time

# *** HashTable_3 (start) ***

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
    def __init__(self,initial_bucket_size=14293):
        # Note: Use prime number for bucket_size to reduce hash conflicts.
        # Note: rehash to fit data size¸
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
# *** HashTable_3 (finish) ***

# *** An item object ***
# represents one key - value pair in the hash table.
    # |url|: The url of the item. 
    # |contents|: The content of the item. The value must be string??
    # |prev|: The previous item in the doubly linked list. 
    # |next|: The next item in the doubly linked list. If this is the last item in the
    #         linked list, |next| is None.
class Node:
    def __init__(self, url, contents):
        self.url = url
        self.contents = contents
        self.prev = None
        self.next = None

class Cache:
    # *** Initialize the cache. ***
    # |n|: The size of the cache.
    # |current_size|: the size of item 
    # hash_table is class HashTable() 
    # |head|: most recentry acsessed page.
    # |tail|: oldest page.
    def __init__(self, n):
        self.capacity = n
        self.current_size = 0
        self.hash_table = HashTable()
        self.head = None
        self.tail = None
    # *** change the order of cache ***
    # |node|: most recentry acessed one.
    def _move_to_front(self, node):
        # 1) node exist at head already.
        if node == self.head:
            return
        # 2) node exist in list. -> delete and add to head
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        
        # もしノードがテールだった場合、テールを更新
        if node == self.tail:
            self.tail = node.prev
        
        # ノードを先頭に移動
        node.next = self.head
        node.prev = None
        if self.head:
            self.head.prev = node
        self.head = node
        # リストが空だった場合（つまり最初のノードが追加された場合）
        if not self.tail:
            self.tail = node


    # ヘルパー関数: ノードをリストから削除する
    def _remove_node(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        self.current_size -= 1
    
    # Access a page and update the cache so that it stores the most recently
    # accessed N pages. This needs to be done with mostly O(1).
    # |url|: The accessed URL
    # |contents|: The contents of the URL
    def access_page(self, url, contents):
        # ハッシュテーブルでURLを検索
        result, found = self.hash_table.get(url)

        if found:
            # URLがキャッシュに存在する場合
            node = result # HashTableに保存されているのはNodeオブジェクト
            node.contents = contents # コンテンツを更新（テストケースにはないが、現実的）
            self._move_to_front(node) # リストの先頭に移動
        else:
            # URLがキャッシュに存在しない場合
            new_node = Node(url, contents)

            if self.current_size >= self.capacity:
                # キャッシュが満杯の場合、最も古いページを削除
                if self.tail: # テールが存在することを確認
                    self.hash_table.delete(self.tail.url) # ハッシュテーブルから削除
                    self._remove_node(self.tail) # リストから削除

            # 新しいノードをリストの先頭に追加
            new_node.next = self.head
            if self.head:
                self.head.prev = new_node
            self.head = new_node
            if not self.tail: # リストが空だった場合
                self.tail = new_node
            self.hash_table.put(url, new_node) # ハッシュテーブルに追加
            self.current_size += 1

    # Return the URLs stored in the cache. The URLs are ordered in the order
    # in which the URLs are mostly recently accessed.
    def get_pages(self):
        pages = []
        current = self.head
        while current:
            pages.append(current.url)
            current = current.next
        return pages


def cache_test():
    # Set the size of the cache to 4.
    cache = Cache(4)

    # Initially, no page is cached.
    assert cache.get_pages() == []

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # "a.com" is cached.
    assert cache.get_pages() == ["a.com"]

    # Access "b.com".
    cache.access_page("b.com", "BBB")
    # The cache is updated to:
    #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["b.com", "a.com"]

    # Access "c.com".
    cache.access_page("c.com", "CCC")
    # The cache is updated to:
    #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["c.com", "b.com", "a.com"]

    # Access "d.com".
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "d.com" again.
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "a.com" again.
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "d.com", "c.com", "b.com"]

    cache.access_page("c.com", "CCC")
    assert cache.get_pages() == ["c.com", "a.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is full, so we need to remove the least recently accessed page "b.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "a.com", "c.com", "d.com"]

    # Access "f.com".
    cache.access_page("f.com", "FFF")
    # The cache is full, so we need to remove the least recently accessed page "c.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["f.com", "e.com", "a.com", "c.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "f.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "f.com", "a.com", "c.com"]

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "e.com", "f.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "e.com", "f.com", "c.com"]

    print("Tests passed!")


if __name__ == "__main__":
    cache_test()
