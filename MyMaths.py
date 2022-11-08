import math

def max(val1, val2):
    if val1 > val2:
        return val1
    return val2

def min(val1, val2):
    if val1 < val2:
        return val1
    return val2

def clamp(val, min_val, max_val):
    return max(min_val, min(max_val, val))

def sign(val):
    if val == 0:
        return val
        
    return val/abs(val)