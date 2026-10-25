import numpy as np


def gen_random_array(size: int) -> np.ndarray:
    return np.random.randint(0, 100000, size, dtype=np.int32)


def gen_nearly_sorted_array(size: int, noise_percent: float = 0.05) -> np.ndarray:
    arr = np.arange(size, dtype=np.int32)
    num_swaps = int(size * noise_percent)
    
    # Apply random swaps to create noise
    idx1 = np.random.randint(0, size, num_swaps)
    idx2 = np.random.randint(0, size, num_swaps)
    
    arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
    return arr


def gen_reverse_sorted_array(size: int) -> np.ndarray:
    return np.arange(size, 0, -1, dtype=np.int32)

