"""
Given a cell with "it's a fib sequence" from slideshow,
    please write function "check_fib", which accepts a Sequence of integers, and
    returns if the given sequence is a Fibonacci sequence

We guarantee, that the given sequence contain >= 0 integers inside.

"""
from collections import Sequence

def check_fib(sequence: Sequence[int]) -> bool:
    if len(sequence) < 2:
        return False
   
    if sequence[0] != 0 or sequence[1] != 1:
        return False
        
    if len(sequence) == 2:
        return True
    
    for i in range(2, len(sequence)):
        if sequence[i] != sequence[i-1] + sequence[i-2]:
            return False
    
