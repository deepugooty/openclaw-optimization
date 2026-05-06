def find_two_sum(numbers, target):
    """
    Find two numbers in the list that sum to the target.
    
    Args:
        numbers: List of numbers (could be empty or contain duplicates)
        target: The target sum to find
    
    Returns:
        List of two numbers that sum to the target, or [] if not found
    
    Raises:
        ValueError: If numbers is empty or target is not an integer
    """
    # Validate input
    if not isinstance(numbers, list):
        raise TypeError("numbers must be a list")
    if len(numbers) == 0:
        raise ValueError("numbers cannot be empty")
    
    if not isinstance(target, int) or isinstance(target, bool):
        raise ValueError("target must be an integer")
    
    # Convert to float to handle negative numbers properly
    numbers = [float(n) for n in numbers]
    
    # Sort to allow two-pointer approach
    numbers.sort()
    
    # Two-pointer approach
    left, right = 0, len(numbers) - 1
    
    while left < right:
        current_sum = numbers[left] + numbers[right]
        
        if current_sum == target:
            return [numbers[left], numbers[right]]
        
        elif current_sum < target:
            left += 1
        else:
            right -= 1
            
    return []

# Example usage:
# print(find_two_sum([1, 2, 4, 8, 6]))  # Expected: [1, 4] or [2, 6] (order may vary)
# print(find_two_sum([]))               # Should raise ValueError
