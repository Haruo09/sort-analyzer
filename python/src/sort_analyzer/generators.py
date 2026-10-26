import numpy as np

def gen_random_array(size: int, min_val: int = 0, max_val: int = 1_000_000) -> np.ndarray:
    return np.random.randint(min_val, max_val, size=size, dtype=np.int32)

def gen_sorted_array(size: int) -> np.ndarray:
    return np.arange(size, dtype=np.int32)

def gen_reverse_sorted_array(size: int) -> np.ndarray:
    return np.arange(size, 0, -1, dtype=np.int32)

def gen_nearly_sorted_array(size: int, swap_ratio: float = 0.025) -> np.ndarray:
    arr = gen_sorted_array(size)
    num_swaps = int(size * swap_ratio)
    for _ in range(num_swaps):
        i, j = np.random.randint(0, size, size=2)
        arr[i], arr[j] = arr[j], arr[i]
    return arr
