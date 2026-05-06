from find_pair import find_pair

# Example usage
if __name__ == "__main__":
    # Example test cases from original requirements
    print("Normal case test:")
    result = find_pair([1, 2, 3, 4, 5], 4)
    print(f"  find_pair([1, 2, 3, 4, 5], 4) = {result}")
    
    print("No solution test:")
    result = find_pair([1, 2, 3, 4, 5], 7)
    print(f"  find_pair([1, 2, 3, 4, 5], 7) = {result}")
    
    print("Duplicate numbers test:")
    result = find_pair([1, 2, 2, 2, 3], 4)
    print(f"  find_pair([1, 2, 2, 2, 3], 4) = {result}")
    
    print("Negative numbers test:")
    result = find_pair([-1, 0, 1, 2, 3, 4, 5], 4)
    print(f"  find_pair([-1, 0, 1, 2, 3, 4, 5], 4) = {result}")
    
    print("Small input edge case test:")
    result = find_pair([1, 2, 3], 4)
    print(f"  find_pair([1, 2, 3], 4) = {result}")
    result = find_pair([1, 2, 3, 4, 5], 9)
    print(f"  find_pair([1, 2, 3, 4, 5], 9) = {result}")
