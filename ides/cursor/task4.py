import random
import time
import sys
from typing import List

def find_kth_largest(nums: List[int], k: int) -> int:
    """
    使用QuickSelect算法找到数组中第k大的元素
    
    参数:
        nums: 整数数组
        k: 第k大元素的k值（1 <= k <= len(nums)）
    
    返回:
        第k大的元素
    """
    if not nums or k < 1 or k > len(nums):
        raise ValueError("无效的输入：数组为空或k值不合法")
    
    # 转换为第k小的索引（0-based）
    k = len(nums) - k
    
    return quick_select(nums, 0, len(nums) - 1, k)

def quick_select(nums: List[int], left: int, right: int, k_smallest: int) -> int:
    """
    QuickSelect核心算法实现
    
    参数:
        nums: 整数数组
        left: 当前考察区间的左边界
        right: 当前考察区间的右边界
        k_smallest: 要找的第k小元素的索引
    
    返回:
        数组中第k小的元素
    """
    # 如果区间只有一个元素，直接返回
    if left == right:
        return nums[left]
    
    # 随机选择枢轴索引，减少最坏情况出现的概率
    pivot_index = random.randint(left, right)
    
    # 将枢轴元素放到正确位置，并返回其索引
    pivot_index = partition(nums, left, right, pivot_index)
    
    # 根据枢轴位置与k的关系决定下一步
    if k_smallest == pivot_index:
        # 找到了第k小的元素
        return nums[k_smallest]
    elif k_smallest < pivot_index:
        # 第k小的元素在左半部分
        return quick_select(nums, left, pivot_index - 1, k_smallest)
    else:
        # 第k小的元素在右半部分
        return quick_select(nums, pivot_index + 1, right, k_smallest)

def partition(nums: List[int], left: int, right: int, pivot_index: int) -> int:
    """
    对数组区间进行分区，小于枢轴的元素放左边，大于枢轴的元素放右边
    
    参数:
        nums: 整数数组
        left: 区间左边界
        right: 区间右边界
        pivot_index: 选择的枢轴索引
    
    返回:
        枢轴元素的最终位置
    """
    pivot = nums[pivot_index]
    
    # 将枢轴元素移到最右边
    nums[pivot_index], nums[right] = nums[right], nums[pivot_index]
    
    # 存储最终枢轴应该在的位置
    store_index = left
    
    # 将小于枢轴的元素放到左边
    for i in range(left, right):
        if nums[i] < pivot:
            nums[store_index], nums[i] = nums[i], nums[store_index]
            store_index += 1
    
    # 将枢轴元素放到最终位置
    nums[right], nums[store_index] = nums[store_index], nums[right]
    
    return store_index

def generate_large_array(size: int, min_val: int = 0, max_val: int = 10**9) -> List[int]:
    """
    生成指定大小的随机整数数组，用于测试
    
    参数:
        size: 数组大小
        min_val: 最小值
        max_val: 最大值
    
    返回:
        随机整数数组
    """
    return [random.randint(min_val, max_val) for _ in range(size)]

def benchmark(arr: List[int], k: int) -> float:
    """
    测量查找第k大元素的时间
    
    参数:
        arr: 输入数组
        k: 第k大元素的k值
    
    返回:
        执行时间（秒）
    """
    start_time = time.time()
    result = find_kth_largest(arr, k)
    end_time = time.time()
    return end_time - start_time, result

# 示例和测试
if __name__ == "__main__":
    # 基本示例
    arr = [3, 2, 1, 5, 6, 4]
    k = 2
    result = find_kth_largest(arr, k)
    print(f"数组 {arr} 中第 {k} 大的元素是: {result}")
    
    # 验证结果正确性
    sorted_arr = sorted(arr, reverse=True)
    print(f"排序后的数组(从大到小): {sorted_arr}")
    print(f"验证: 排序后第 {k} 个元素是: {sorted_arr[k-1]}")
    
    # 性能测试（小规模）
    test_size = 10**5
    print(f"\n生成大小为 {test_size} 的随机数组...")
    large_arr = generate_large_array(test_size)
    
    # 测试不同k值
    for test_k in [1, test_size // 2, test_size]:
        execution_time, result = benchmark(large_arr.copy(), test_k)
        print(f"查找第 {test_k} 大元素耗时: {execution_time:.6f} 秒, 结果: {result}")
    
    # 与排序方法比较（小规模）
    start_time = time.time()
    sorted_result = sorted(large_arr, reverse=True)[k-1]
    sort_time = time.time() - start_time
    print(f"使用排序方法耗时: {sort_time:.6f} 秒")
    
    # 展示内存优势（原地操作）
    print("\n内存使用优势: QuickSelect是原地算法，不需要额外的O(n)空间")
    
    # 可选: 超大规模测试
    print("\n注意: 实际应用中可以处理1000万元素，这里为了演示而使用较小规模")
    print("若要测试1000万元素，请取消下面代码的注释并运行")
    
    """
    # 超大规模测试 (解除注释运行)
    huge_size = 10**7  # 1000万元素
    print(f"\n生成大小为 {huge_size} 的随机数组...")
    huge_arr = generate_large_array(huge_size)
    
    huge_k = 1000000  # 找第100万大的元素
    execution_time, result = benchmark(huge_arr, huge_k)
    print(f"从1000万元素中查找第 {huge_k} 大元素耗时: {execution_time:.6f} 秒, 结果: {result}")
    """ 