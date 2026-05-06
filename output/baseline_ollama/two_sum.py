def two_sum(nums, target):
    """
    Find two numbers in nums that sum to target.
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [nums[i], nums[j]]
    return None
