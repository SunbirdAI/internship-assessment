from typing import List
# todo
# create a list that stores the returned values
# check if n is even first
#  got to the odd part
# wrap the logic in a loop

def collatz(n: int) -> List[int]:
    # list
    returnedresults = [n]

    # check if the current value of n is not 1 else iterate over the list
    while( n !=1):
     
     
    #  check if vaalue of n is even
     if(n %2 == 0 ):
        #  debugging
        #  print("current value of n is ===== "+ n ) 
         n = n/2
        #  if n is not even then perform the odd operation
     else:
        n = ((n*3)+1)

    # append the results of each operation to our result sequence

     returnedresults.append(n)
    #  debugging
    #  print(returnedresults)

    return returnedresults





    """
    You're given a positive integer n. Write an algorithm that does the following:
        - If n is even, the algorithm divides n by 2. This is the new value of n
        - If n is odd, the algorithm multiplies it by 3 and adds 1. This is the new value of n.
        - The algorithm repeats this until n == 1.

    Implement this algorithm in this function and return a list of all the intermediate values of n.
    For example, if n = 3, the sequence of values is: 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1
    So, your function would return: [3, 10, 5, 16, 8, 4, 2, 1]
    """
    


def distinct_numbers(numbers: List[int]) -> int:
    # Todo
    # check if the availble list is not null
    # create a list of unqiue numbers
    # count the unique numbers

    # list of unqiue numbers
    Unnumbers = []

# chek to see if the availbe list is not null
    number_of_items_in_list = len(numbers)
    while( number_of_items_in_list != 0):
       for i in numbers:
          Unnumbers.add(i)

    return len(Unnumbers)
       
 

    """
    You are given a list of integers (the list could be empty),
      calculate the number of distinct/unique values in the list.

    E.g if numbers = [2, 3, 2, 2, 3], 
    then the answer is 2 since there are only 2 unique numbers: 2 and 3.
    """
    
