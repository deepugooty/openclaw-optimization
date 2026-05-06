# Python implementation of finding two numbers in a list that sum to a target
def numbers_to_target(numbers, target):
    """
    Find two numbers in a list that sum to a target.
    
    Args:
        numbers: A list of integers
        target: The sum of the two numbers
    
    Returns:
        A list of the two numbers, or an empty list if no such pair exists
    """
    if len(numbers) < 2:
        return []
    
    # Sort to allow O(n^2) approach
    numbers.sort()
    
    # Two pointers approach
    left, right = 0, len(numbers) - 1
    
    while left < right:
        current_sum = numbers[left] + numbers[right]
        
        if current_sum == target:
            return [numbers[left], numbers[right]]
        
        if current_sum < target:
            # Need larger sum, move right pointer
            left += 1
        else:
            # Need smaller sum, move left pointer
            right -= 1
    
    return []
