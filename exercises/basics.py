from typing import List

def collatz(n: int) -> List[int]:
    """
    Calculates the Collatz sequence for a given positive integer n.
    
    The algorithm does the following:
        - If n is even, divides n by 2.
        - If n is odd, multiplies it by 3 and adds 1.
        - Repeats this until n == 1.

    Args:
        n (int): The starting positive integer.

    Returns:
        List[int]: A list of all intermediate values of n in the sequence, 
                   starting with the original number and ending with 1.
    """
    sequence = [n]
    
    # Continue generating the sequence until we reach 1
    while n != 1:
        if n % 2 == 0:
            # For even numbers, use integer division by 2
            n = n // 2
        else:
            # For odd numbers, multiply by 3 and add 1
            n = n * 3 + 1
            
        sequence.append(n)
        
    return sequence 

def distinct_numbers(numbers: List[int]) -> int:
    """
    Calculates the number of distinct (unique) values in a given list of integers.

    Args:
        numbers (List[int]): A list of integers (can be empty).

    Returns:
        int: The count of unique integers in the list.
    """
    # A set automatically filters out duplicate values, leaving only unique elements
    unique = set(numbers)
    return len(unique)

# ==========================================
# Testing the implementations
# ==========================================

# 1. Check the Collatz sequence for n = 7
collatz_result = collatz(7)
print("The Collatz sequence for 7 is:", collatz_result)

# 2. Check the distinct numbers function
distinct_result = distinct_numbers([1, 1, 1, 2, 2, 4, 4, 3, 9, 6, 6])
print("The number of unique values is:", distinct_result)