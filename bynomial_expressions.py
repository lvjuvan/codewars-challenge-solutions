#https://www.codewars.com/kata/540d0fdd3b6532e5c3000b5b


import re
def expand(expr):
    re_result = re.search(r"(?:\()(-?[0-9]*)([a-z])([+-][0-9]*)(?:\)\^)([0-9]*)", expr)
    a, var, b, exponent = re_result.groups()
    print("Expr:" + expr)
    
    print("Exponent: " + exponent)
    print("variable: " + var)
    if a == "-":
        a_int = -1
    elif a is None or a == "":
        a_int = 1
    else:
        a_int = int(a)
    b_int = int(b)
    
    print("Coeff a: " + str(a_int))
    print("Coeff b: " + str(b_int))
    exponent_int = int(exponent)
    if exponent_int == 0:
        return "1"
    #coefficients of polynomial starting on 0 and increasing
    coeffs = [0] * (exponent_int - 1) + [a_int, b_int]
    for i_exp in range(exponent_int-1):
        for i in range(len(coeffs) - 1):
            coeffs[i] = coeffs[i] * b_int + coeffs[i + 1] * a_int
        coeffs[-1] *= b_int
    print(coeffs)
    result = ""
    curr_exp = exponent_int
    for coeff in coeffs:
        
        if coeff == 0:
            curr_exp -= 1
            continue
        sign = "-" if coeff < 0  else ("+" if result != "" else "")
        expl_coeff = str(abs(coeff)) if (abs(coeff) != 1 or curr_exp == 0) else ""
        expl_var = (var if curr_exp > 0 else "") + ("^" + str(curr_exp) if curr_exp > 1 else "")
        result += sign + expl_coeff + expl_var

        curr_exp -= 1
    print(result)
    return result
