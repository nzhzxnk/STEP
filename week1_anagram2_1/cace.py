from itertools import permutations

def up(perm):
    now = perm[0]
    count = 1
    for i in range(9):
        if now < perm[i]:
            count += 1
            now = perm[i]
    return count 

def down(perm):
    now = perm[0]
    count = 1
    for i in range(9):
        if now > perm[i]:
            count += 1
            now = perm[i]
    return count 

nums = list(range(1, 10))
perms = permutations(nums)
min_len = 9
min_perm = None

for perm in perms:
    if min_len > max(up(perm),down(perm)):
        min_len = max(up(perm),down(perm))
        min_perm = perm

print(min_len,min_perm)


# for perm in perms:
#     print(max(up(perm),down(perm)),perm)