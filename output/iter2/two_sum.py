from typing import List, Tuple


def two_sum(nums: List[int], target: int) -> List[Tuple[int, int]]:
    """
    Find indices of two numbers that add up to target.
    Returns exactly one solution if possible.
    """
    if len(nums) < 2:
        return []
    
    # Sort the array for O(n^2) approach
    nums.sort()
    
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                # Return exact one solution and indices in any order
                return (i, j)
    
    return []


# Test cases
if __name__ == "__main__":
    print(two_sum([2, 7, 11, 15], 9))  # Expected: [0, 1]
    print(two_sum([10, -10, 5], 12))   # Expected: [0, 2]
    print(two_sum([-1, 2, -2, 5], 4))  # Expected: [1, 3]
    print(two_sum([], 5))              # Expected: []
    print(two_sum([3, 2], 5))          # Expected: []
    print(two_sum([10, 15, 10], 15))    # Expected: [0, 2]