def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n == 2:
        return 1
    
    if n > 0:
        n_1 = 1
        n_2 = 2
        index = 2
    
        while index < n:
            tmp = n_1
            n_1 = n_2
            n_2 += tmp
            index += 1
        return n_1
    else:
        n_1 = 0
        n_2 = 1
        index = 0
        while index > n:
            new = n_2 - n_1
            n_2 = n_1
            n_1 = new
            index -= 1
        return n_1
