import random

def find_kth_largest(arr, k):
    if not arr or k < 1 or k > len(arr):
        return None
    return quick_select(arr, 0, len(arr) - 1, len(arr) - k)

def quick_select(arr, left, right, k):
    if left == right:
        return arr[left]
    
    pivot_idx = random.randint(left, right)
    pivot_idx = partition(arr, left, right, pivot_idx)
    
    if k == pivot_idx:
        return arr[k]
    elif k < pivot_idx:
        return quick_select(arr, left, pivot_idx - 1, k)
    else:
        return quick_select(arr, pivot_idx + 1, right, k)

def partition(arr, left, right, pivot_idx):
    pivot_value = arr[pivot_idx]
    arr[pivot_idx], arr[right] = arr[right], arr[pivot_idx]
    store_idx = left
    
    for i in range(left, right):
        if arr[i] < pivot_value:
            arr[store_idx], arr[i] = arr[i], arr[store_idx]
            store_idx += 1
            
    arr[right], arr[store_idx] = arr[store_idx], arr[right]
    return store_idx

if __name__ == "__main__":
    # 测试用例
    arr = [3, 2, 1, 5, 6, 4]
    k = 2
    result = find_kth_largest(arr, k)
    print(f"第{k}大的元素是：{result}")
