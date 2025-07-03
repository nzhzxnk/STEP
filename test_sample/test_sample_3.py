def create_beautiful_substring(string,start_index):
    i = 0
    substring_set = set()
    while start_index+i < len(string):
        if not string[start_index+i] in substring_set:
            substring_set.add(string[start_index+i])
            i += 1
        else:
            length = i
            return start_index, length
    length = i
    return start_index, length

def replicate_substring(start_index,length):
    return string[start_index:start_index+length]

if __name__ == "__main__":
    string = input().strip()
    string = string.lower()
    max_start_index = 0
    max_length = 0
    for j in range(len(string)):
        start_index, length = create_beautiful_substring(string, j)
        if length > max_length:
            max_start_index, max_length = start_index, length
    max_substring = replicate_substring(max_start_index, max_length)
    print(max_substring) 
