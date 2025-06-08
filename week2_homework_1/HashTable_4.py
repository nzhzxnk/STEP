# This file is 4th ver. 

#  *** Progress ***
# 25/06/05 21:20 edit comment now

# *** what is the changes? ***
# hash table -> AVL tree

import random, sys, time

# *** Node object ***
class Node:
    # |key|: The key of the item. The key must be a string.
    # |value|: The value of the item. The value can be any type.
    # The children item(left, right) in the binary tree.
    def __init__(self, key, value):
        assert type(key) == str
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 0

# *** AVL tree ***
# represents balanced binary tree.
# Note: The key must be a string. The value can be any type.
class AVLTree:
    # *** Initialize the AVL tree. ***
    # self.item_count: The total number of items in the AVL tree.
    def __init__(self):
        self.root = None
        self.item_count = 0
    # *** check node height ***
    def _get_height(self, node):
        if not node:
            return -1
        return node.height
    # *** update parent node height ***
    # get larger one in left child height and right child height.
    def _update_height(self, node):
        if node is None:
            return
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
    # *** check balance of AVL tree. ***
    def _get_balance_factor(self, node):
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    # *** Rotate right (top node move left) ***
    def _right_rotate(self, z_node):
        y_node = z_node.left
        T2 = y_node.right
        y_node.right = z_node
        z_node.left = T2
        self._update_height(z_node)
        self._update_height(y_node)
        return y_node
    # *** Rotate left (top node move right) ***
    def _left_rotate(self, z_node):
        y_node = z_node.right
        T2 = y_node.left
        y_node.left = z_node
        z_node.right = T2
        self._update_height(z_node)
        self._update_height(y_node)
        return y_node
    
    def _find_min_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    # *** check the tree size ***
    def size(self):
        return self.item_count
    # *** put new node ***
    # |key|: The key of the item. The key must be a string.
    # |value|: The value of the item. The value can be any type.
    # The children item(left, right) in the binary tree.
    def put(self, key, value):
        is_new_key_tracker = [False] 
        self.root = self._put_recursive(self.root, key, value, is_new_key_tracker)
        if is_new_key_tracker[0]:
            self.item_count += 1
            return True
        else:
            return False

    def _put_recursive(self, current_node, key, value, is_new_key_tracker):
        if current_node is None:
            is_new_key_tracker[0] = True
            return Node(key, value)

        if key < current_node.key:
            current_node.left = self._put_recursive(current_node.left, key, value, is_new_key_tracker)
        elif key > current_node.key:
            current_node.right = self._put_recursive(current_node.right, key, value, is_new_key_tracker)
        else:
            current_node.value = value
            is_new_key_tracker[0] = False
            return current_node

        self._update_height(current_node)
        balance = self._get_balance_factor(current_node)

        if balance > 1: # Left Heavy
            if self._get_balance_factor(current_node.left) >= 0: # LL Case
                return self._right_rotate(current_node)
            else: # LR Case
                current_node.left = self._left_rotate(current_node.left)
                return self._right_rotate(current_node)

        if balance < -1: # Right Heavy
            if self._get_balance_factor(current_node.right) <= 0: # RR Case
                return self._left_rotate(current_node)
            else: # RL Case
                current_node.right = self._right_rotate(current_node.right)
                return self._left_rotate(current_node)

        return current_node

    def get(self,key):
        target = self.get_recursion(self.root,key)
        if target is None:
            return (target, False)
        else:
            return (target, True)
            
    def get_recursion(self,cur_node,key):
        if cur_node is None:
            return None 
        if cur_node.key == key:
            return cur_node.value
        if cur_node.key < key: # Search key is greater, go right
            return self.get_recursion(cur_node.right, key)
        else: # Search key is smaller, go left
            return self.get_recursion(cur_node.left, key)
        # This line was logically unreachable and has been removed

    def delete(self, key):
        key_deleted_tracker = [False]
        self.root = self._delete_recursive(self.root, key, key_deleted_tracker)
        if key_deleted_tracker[0]:
            self.item_count -= 1
            return True
        else:
            return False

    def _delete_recursive(self, current_node, key, key_deleted_tracker):
        if current_node is None:
            key_deleted_tracker[0] = False
            return None

        if key < current_node.key:
            current_node.left = self._delete_recursive(current_node.left, key, key_deleted_tracker)
        elif key > current_node.key:
            current_node.right = self._delete_recursive(current_node.right, key, key_deleted_tracker)
        else:
            key_deleted_tracker[0] = True
            if current_node.left is None:
                temp_node = current_node.right
                # current_node = None # Not strictly necessary in Python for GC
                return temp_node
            elif current_node.right is None:
                temp_node = current_node.left
                # current_node = None # Not strictly necessary
                return temp_node
            
            successor_node = self._find_min_node(current_node.right)
            current_node.key = successor_node.key
            current_node.value = successor_node.value
            current_node.right = self._delete_recursive(current_node.right, successor_node.key, [False])

        if current_node is None:
            return None

        self._update_height(current_node)
        balance = self._get_balance_factor(current_node)

        if balance > 1: # Left Heavy
            if self._get_balance_factor(current_node.left) >= 0: # LL Case
                return self._right_rotate(current_node)
            else: # LR Case
                current_node.left = self._left_rotate(current_node.left)
                return self._right_rotate(current_node)

        if balance < -1: # Right Heavy
            if self._get_balance_factor(current_node.right) <= 0: # RR Case
                return self._left_rotate(current_node)
            else: # RL Case
                current_node.right = self._right_rotate(current_node.right)
                return self._left_rotate(current_node)

        return current_node

# *** Test the functional behavior of the AVL tree. ***
# Changed: for AVL tree
def functional_test():
    avl_tree = AVLTree() 

    assert avl_tree.put("aaa", 1) == True
    assert avl_tree.get("aaa") == (1, True)
    assert avl_tree.size() == 1 

    assert avl_tree.put("bbb", 2) == True
    assert avl_tree.put("ccc", 3) == True
    assert avl_tree.put("ddd", 4) == True
    assert avl_tree.get("aaa") == (1, True)
    assert avl_tree.get("bbb") == (2, True)
    assert avl_tree.get("ccc") == (3, True)
    assert avl_tree.get("ddd") == (4, True)
    assert avl_tree.get("a") == (None, False)
    assert avl_tree.get("aa") == (None, False)
    assert avl_tree.get("aaaa") == (None, False)
    assert avl_tree.size() == 4

    assert avl_tree.put("aaa", 11) == False
    assert avl_tree.get("aaa") == (11, True)
    assert avl_tree.size() == 4

    assert avl_tree.delete("aaa") == True
    assert avl_tree.get("aaa") == (None, False)
    assert avl_tree.size() == 3

    assert avl_tree.delete("a") == False
    assert avl_tree.delete("aa") == False
    assert avl_tree.delete("aaa") == False
    assert avl_tree.delete("aaaa") == False

    assert avl_tree.delete("ddd") == True
    assert avl_tree.delete("ccc") == True
    assert avl_tree.delete("bbb") == True
    assert avl_tree.get("aaa") == (None, False)
    assert avl_tree.get("bbb") == (None, False)
    assert avl_tree.get("ccc") == (None, False)
    assert avl_tree.get("ddd") == (None, False)
    assert avl_tree.size() == 0

    # Test cases that might trigger rotations
    avl_tree = AVLTree()
    keys = ["d", "c", "b", "a", "e", "f", "g"] # LL, RR rotations
    for i, k in enumerate(keys):
        assert avl_tree.put(k, i) == True
    assert avl_tree.size() == len(keys)
    
    # LR / RL rotation checks (example)
    avl_tree = AVLTree()
    assert avl_tree.put("k", 1) == True
    assert avl_tree.put("f", 2) == True
    assert avl_tree.put("h", 3) == True # Should trigger LR rotation (k, f, h) -> h becomes root
    # Add more specific assertions here to check tree structure if needed, or rely on size/get
    assert avl_tree.get("h") == (3, True)
    assert avl_tree.get("f") == (2, True)
    assert avl_tree.get("k") == (1, True)
    assert avl_tree.size() == 3
    
    # Deletion tests that might trigger rotations
    # ... (can be complex to set up specific scenarios without tree printing)

    print("Functional tests passed!")


# *** Test the performance of the AVL tree. ***
def performance_test():
    avl_tree = AVLTree() # Changed from HashTable

    for iteration in range(100): # Reduced iterations for quicker testing if needed
        begin = time.time()
        random.seed(iteration)
        for i in range(10000): # Reduced item count for quicker testing
            rand = random.randint(0, 100000000)
            avl_tree.put(str(rand), str(rand))
        random.seed(iteration)
        for i in range(10000): # Reduced item count
            rand = random.randint(0, 100000000)
            avl_tree.get(str(rand))
        end = time.time()
        print("%d %.6f" % (iteration, end - begin))
    
    print(f"Size before massive delete: {avl_tree.size()}")

    for iteration in range(100): # Reduced iterations
        random.seed(iteration)
        for i in range(10000): # Reduced item count
            rand = random.randint(0, 100000000)
            avl_tree.delete(str(rand))
    
    print(f"Size after massive delete: {avl_tree.size()}")
    if avl_tree.size() != 0:
        print(f"Error: AVL tree not empty after deletes. Size: {avl_tree.size()}")

    assert avl_tree.size() == 0, f"AVLTree size is {avl_tree.size()} instead of 0"
    print("Performance tests passed!")

# *** Test result ***
# Functional tests passed!
# 0 0.092612
# 1 0.105932
# 2 0.109138
# 3 0.112664
# 4 0.117125
# 5 0.117727
# 6 0.121797
# 7 0.121735
# 8 0.128206
# 9 0.125004
# 10 0.128212
# 11 0.130480
# 12 0.129883
# 13 0.132182
# 14 0.130945
# 15 0.131767
# 16 0.134611
# 17 0.133998
# 18 0.136652
# 19 0.136201
# 20 0.137897
# 21 0.136607
# 22 0.136894
# 23 0.139731
# 24 0.138489
# 25 0.248817
# 26 0.142050
# 27 0.140612
# 28 0.142918
# 29 0.141483
# 30 0.145068
# 31 0.144443
# 32 0.143332
# 33 0.146495
# 34 0.144338
# 35 0.146076
# 36 0.147539
# 37 0.145195
# 38 0.148489
# 39 0.145902
# 40 0.148493
# 41 0.146581
# 42 0.149796
# 43 0.146986
# 44 0.147464
# 45 0.150631
# 46 0.148340
# 47 0.150850
# 48 0.149343
# 49 0.149031
# 50 0.152127
# 51 0.149981
# 52 0.480210
# 53 0.151896
# 54 0.151534
# 55 0.153946
# 56 0.151946
# 57 0.157992
# 58 0.153545
# 59 0.154896
# 60 0.153110
# 61 0.153443
# 62 0.155723
# 63 0.153102
# 64 0.155946
# 65 0.153833
# 66 0.154254
# 67 0.156789
# 68 0.154502
# 69 0.199981
# 70 0.155769
# 71 0.157970
# 72 0.155675
# 73 0.155637
# 74 0.158917
# 75 0.156489
# 76 0.158372
# 77 0.157104
# 78 0.157441
# 79 0.763878
# 80 0.157667
# 81 0.159420
# 82 0.157728
# 83 0.157259
# 84 0.160675
# 85 0.161038
# 86 0.160494
# 87 0.158813
# 88 0.159110
# 89 0.162155
# 90 0.159029
# 91 0.161483
# 92 0.159601
# 93 0.161744
# 94 0.159981
# 95 0.159574
# 96 0.162718
# 97 0.160551
# 98 0.162825
# 99 0.161190
# Size before massive delete: 994949
# Size after massive delete: 0
# Performance tests passed!

if __name__ == "__main__":
    functional_test()
    performance_test()