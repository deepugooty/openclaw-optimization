import pytest

def test_find_pair_normal_case():
    """Normal case with multiple pairs."""
    assert find_pair([1, 2, 3, 4, 5], 4) == (1, 5)
    assert find_pair([3, 2, 1, 4], 5) == (1, 4)
    assert find_pair([5, 4, 3, 2, 1], 10) == (1, 5)
    assert find_pair([1, 1, 1, 1], 2) == (0, 2)
    assert find_pair([1, 1, 1, 1], 3) == (0, 3)


def test_find_pair_no_solution():
    """Case with no valid pairs."""
    assert find_pair([1, 2, 3, 4, 5], 7) is None
    assert find_pair([1, 2, 3, 4], 5) is None


def test_find_pair_duplicate_numbers():
    """Handles duplicate values and prevents using the same index twice."""
    assert find_pair([1, 2, 2, 2, 3], 4) is None
    assert find_pair([1, 2, 3, 2, 3], 5) == (2, 3)


def test_find_pair_negative_numbers():
    """Handles negative numbers correctly."""
    assert find_pair([-1, 0, 1, 2, 3, 4, 5], 4) == (-1, 3)
    assert find_pair([-1], None) is None
    assert find_pair([-2, -1, 0, 1], None) is None


def test_find_pair_small_input_edge_case():
    """Handles very small input lists."""
    assert find_pair([], None) is None
    assert find_pair([1, 2], 3) is None
    assert find_pair([1, 2, 3], 4) is None
    assert find_pair([1, 2, 3, 4, 5], 9) == (0, 5)
