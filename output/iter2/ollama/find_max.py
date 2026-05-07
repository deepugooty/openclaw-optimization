def find_max(numbers):
    """
    Find the maximum value in a list of numbers.
    
    Args:
        numbers (list): A list of numeric values.
        
    Returns:
        int or float: The maximum value found in the list.
        
    Raises:
        ValueError: If the list is empty.
    """
    # Edge Case 1: Empty list
    if not numbers:
        raise ValueError("List cannot be empty.")
    
    # Edge Case 2: Single element
    if len(numbers) == 1:
        return numbers[0]
    
    # Edge Case 3: Negative numbers
    if all(num < 0 for num in numbers):
        return float('-inf')
    
    # Edge Case 4: All negative numbers
    if all(num < 0 for num in numbers):
        return float('-inf')
    
    # Edge Case 5: All positive numbers
    if all(num > 0 for num in numbers):
        return float('inf')
    
    # General case: Find the maximum
    max_val = max(numbers)
    return max_val
