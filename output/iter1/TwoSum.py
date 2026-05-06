def two_sum(nums, target):
    """
    Return indices of two numbers such that nums[i] + nums[j] == target
    - Exactly one solution guaranteed
    - Cannot use the same element twice
    - Indices in any order
    """
    if len(nums) < 2:
        return []
    
    result = []
    
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                result.append((i, j))
                break
        
        if result:
            break
            
    return result
