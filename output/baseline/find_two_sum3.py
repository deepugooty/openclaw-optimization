def two_sum(nums, target):
    """
    Finds two numbers in nums that sum to target.
    
    Args:
        nums: List of integers
        target: The sum target
        
    Returns:
        [left, right] or [None, None] if not found
    """
    if not nums:
        return [None, None]
    
    seen = {}
    left = target
    
    for num in nums:
        # Optimization: if we've already seen the difference (right - left)
        right = left - num
        if right in seen:
            return [seen[right], num]
        
        # Also check if left is in seen (since we're finding pairs)
        if left in seen:
            return [left, num]
        
        seen[left] = num
    
    return [None, None]
