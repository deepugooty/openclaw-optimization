def sum_to_target(nums, target):
    """
    Find two numbers in the list that sum to the given target.

    Args:
        nums (list): List of integers.
        target (int): The target sum to find.

    Returns:
        tuple: (first_number, second_number) if found, otherwise (None, None).
    """
    # Sort the list to make it easier to find the pair
    nums.sort()
    
    # Two-pointer approach
    left = 0
    right = len(nums) - 1
    
    while left < right:
        current_sum = nums[left] + nums[right]
        
        if current_sum == target:
            return (nums[left], nums[right])
        
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return (None, None)
