def find_pair(nums, target):
    if not nums:
        return None
    if len(nums) == 1:
        return None
    
    # Use a hash map to store the first index of each number
    num_to_index = {}
    
    for i in range(len(nums)):
        if nums[i] in num_to_index:
            return num_to_index[nums[i]], i
        
        num_to_index[nums[i]] = i
    
    return None
