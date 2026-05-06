def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Find two numbers in nums that sum up to target.
    
    Args:
        nums: List of integers
        target: Target sum
    
    Returns:
        List of indices of the two numbers that sum to target
    """
    # Dictionary to store the index of each number seen so far
    index_map = {}
    
    # Iterate through the list
    for i, num in enumerate(nums):
        # Calculate the complement needed
        complement = target - num
        
        # Check if complement exists in our map
        if complement in index_map:
            # Return the indices of both numbers
            return [index_map[complement], i]
        
        # Add current number to map with its index
        index_map[num] = i
    
    # If no solution found (should not happen with valid input)
    return []
