def two_sum(nums, target):
    """
    Find two numbers in the list that add up to the target.
    
    Args:
        nums: List of integers
        target: Target sum
    
    Returns:
        List of indices of the two numbers that add up to the target
    """
    left = 0
    right = len(nums) - 1
    
    while left < right:
        current_sum = nums[left] + nums[right]
        
        if current_sum == target:
            return [left, right]
        
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return None


# Example usage:
if __name__ == "__main__":
    nums = [2, 7, 11, 15]
    target = 9
    result = two_sum(nums, target)
    print(f"Indices: {result}")  # Output: [0, 1]
