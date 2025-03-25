"""
Task 4: Performance Optimization and Resource Management
Finding kth largest element in a large array using QuickSelect algorithm.

The algorithm achieves O(n) average time complexity and uses in-place operations
to minimize memory usage, making it suitable for very large arrays.
"""
import random
import time
import sys
from typing import List


def find_kth_largest(arr: List[int], k: int) -> int:
    """
    Find the kth largest element in an array using QuickSelect algorithm.
    
    Args:
        arr: Input array of integers
        k: Position of the element to find (1-based index)
        
    Returns:
        The kth largest element
        
    Raises:
        ValueError: If k is out of bounds or array is empty
    """
    if not arr:
        raise ValueError("Array cannot be empty")
    
    if k < 1 or k > len(arr):
        raise ValueError(f"k must be between 1 and {len(arr)}")
    
    # Convert to 0-based index for internal use
    return _quick_select(arr, 0, len(arr) - 1, len(arr) - k)


def _quick_select(arr: List[int], left: int, right: int, k_smallest: int) -> int:
    """
    Internal QuickSelect implementation with in-place partitioning.
    
    Args:
        arr: Input array
        left: Left boundary index
        right: Right boundary index
        k_smallest: Index of the element to find (0-based)
        
    Returns:
        The element at the k_smallest position after the array is sorted
    """
    # Base case: only one element
    if left == right:
        return arr[left]
    
    # Choose a random pivot to avoid worst-case scenarios on nearly sorted arrays
    pivot_idx = random.randint(left, right)
    
    # Move pivot to the correct position in the array
    pivot_idx = _partition(arr, left, right, pivot_idx)
    
    # If we found the exact position
    if k_smallest == pivot_idx:
        return arr[k_smallest]
    # If k is smaller, search in the left part
    elif k_smallest < pivot_idx:
        return _quick_select(arr, left, pivot_idx - 1, k_smallest)
    # If k is larger, search in the right part
    else:
        return _quick_select(arr, pivot_idx + 1, right, k_smallest)


def _partition(arr: List[int], left: int, right: int, pivot_idx: int) -> int:
    """
    Partition the array around the pivot and return the final pivot position.
    This is an in-place operation to save memory.
    
    Args:
        arr: Input array
        left: Left boundary index
        right: Right boundary index
        pivot_idx: Index of the chosen pivot
        
    Returns:
        The final position of the pivot after partitioning
    """
    pivot_value = arr[pivot_idx]
    
    # Move pivot to the end
    arr[pivot_idx], arr[right] = arr[right], arr[pivot_idx]
    
    # Store index position for elements less than pivot
    store_idx = left
    
    # Move all elements smaller than pivot to the left
    for i in range(left, right):
        if arr[i] < pivot_value:
            arr[i], arr[store_idx] = arr[store_idx], arr[i]
            store_idx += 1
    
    # Move pivot to its final place
    arr[store_idx], arr[right] = arr[right], arr[store_idx]
    
    return store_idx


def benchmark(n: int = 10_000_000, k: int = 1000) -> None:
    """
    Benchmark the algorithm with a large array.
    
    Args:
        n: Size of the array
        k: The k value for finding the kth largest element
    """
    print(f"Generating array with {n:,} elements...")
    arr = [random.randint(0, n) for _ in range(n)]
    
    # Memory usage before running the algorithm
    memory_before = sys.getsizeof(arr)
    print(f"Array size in memory: {memory_before / (1024 * 1024):.2f} MB")
    
    # Benchmark QuickSelect
    start_time = time.time()
    result = find_kth_largest(arr, k)
    end_time = time.time()
    
    print(f"The {k}-th largest element is: {result}")
    print(f"QuickSelect execution time: {end_time - start_time:.4f} seconds")
    
    # Compare with sorting (much slower for large arrays)
    if n <= 1_000_000:  # Only for smaller arrays to avoid excessive runtime
        start_time = time.time()
        sorted_result = sorted(arr, reverse=True)[k-1]
        end_time = time.time()
        
        print(f"Sort-based result: {sorted_result}")
        print(f"Sort-based execution time: {end_time - start_time:.4f} seconds")
        print(f"Verification: Results match = {result == sorted_result}")


if __name__ == "__main__":
    # Example from the problem statement
    arr = [3, 2, 1, 5, 6, 4]
    k = 2
    result = find_kth_largest(arr, k)
    print(f"Example: {k}nd largest element in {arr} is {result}")
    
    # Run with small array for verification
    arr_small = [7, 10, 4, 3, 20, 15]
    k_small = 3
    result_small = find_kth_largest(arr_small, k_small)
    print(f"Verification: {k_small}rd largest element in {arr_small} is {result_small}")
    
    # Run benchmark with large array
    # Using a smaller size to avoid excessive runtime
    print("\nRunning benchmark with large array...")
    benchmark(n=1_000_000, k=50000)  # 1 million elements instead of 10 million for faster execution
