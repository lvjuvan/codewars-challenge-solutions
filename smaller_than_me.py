'''
Takes a list and for each element returns the count of smaller values to the right of said element
'''
def smaller(arr):
    bigger_or_equal_indexes = [None] * len(arr)
    smaller_indexes = [None] * len(arr)
    smaller_count = [0] * len(arr)
    for i in range(len(arr) - 2, -1, -1):
        pointer = i + 1
        while 1:
            if arr[i] == arr[pointer]:
                if bigger_or_equal_indexes[i] is None:
                    bigger_or_equal_indexes[i] = pointer
                if smaller_indexes[i] is None:
                    smaller_indexes[i] = smaller_indexes[pointer]
                smaller_count[i] += smaller_count[pointer]
                break
            elif arr[i] > arr[pointer]:
                if smaller_indexes[i] is None:
                    smaller_indexes[i] = pointer
                if bigger_or_equal_indexes[pointer] is not None:
                    smaller_count[i] += bigger_or_equal_indexes[pointer] - pointer
                    pointer = bigger_or_equal_indexes[pointer]
                else:
                    smaller_count[i] += smaller_count[pointer] + 1
                    break
            else:
                if bigger_or_equal_indexes[i] is None:
                    bigger_or_equal_indexes[i] = pointer
                if smaller_indexes[pointer] is not None:
                    pointer = smaller_indexes[pointer]
                else:
                    break
    return smaller_count
