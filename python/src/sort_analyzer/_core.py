import time
import ctypes
import numpy as np
from scipy.optimize import curve_fit

from ._ffi import get_c_function
from . import generators

# Benchmark Defaults (Can be overridden by CLI flags)
DEFAULT_MIN_SIZE = 1_000
DEFAULT_MAX_SIZE = 100_000
DEFAULT_NUM_STEPS = 10

# Theoretical complexity model for Timsort / O(N log N) algorithms
def timsort_complexity_func(n, a, b):
    return a * n * np.log2(n) + b

# Standardized distribution generators mapping
DISTRIBUTIONS = {
    "random": generators.gen_random_array,
    "nearly_sorted": generators.gen_nearly_sorted_array,
    "reverse_sorted": generators.gen_reverse_sorted_array,
}

# CLI name -> C symbol name mapping
ALGORITHM_SYMBOL_MAP = {
    "timsort": "timSortAlgo",
    "bettertimsort": "betterTimSortAlgo",
    "quicksort": "quickSortAlgo",
    "betterquicksort": "betterQuickSortAlgo",
    "peaktimsort": "peakTimSortAlgo",
}

def get_algorithm_func(algo_name: str):
    """Dynamically fetches and binds the C function based on a CLI string name."""
    if algo_name not in ALGORITHM_SYMBOL_MAP:
        raise ValueError(
            f"Algorithm '{algo_name}' not supported. "
            f"Available: {list(ALGORITHM_SYMBOL_MAP.keys())}"
        )
    symbol_name = ALGORITHM_SYMBOL_MAP[algo_name]
    return get_c_function(symbol_name)

def benchmark_c_func(c_func, sizes: np.ndarray, gen_func) -> np.ndarray:
    """Executes timing benchmarks for a C function across multiple array sizes."""
    times = []
    for size in sizes:
        arr = gen_func(size)
        # Ensure contiguous memory layout for C pointer
        arr_copy = np.ascontiguousarray(arr, dtype=np.int32)
        c_arr = arr_copy.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
        n = len(arr_copy)

        start = time.perf_counter()
        c_func(c_arr, n)
        end = time.perf_counter()

        times.append(end - start)
    return np.array(times)

def run_single_complexity(
    algo_name: str,
    min_size: int = DEFAULT_MIN_SIZE,
    max_size: int = DEFAULT_MAX_SIZE,
    num_steps: int = DEFAULT_NUM_STEPS,
) -> dict:
    """Executes benchmarks and curve fitting for a single algorithm."""
    c_func = get_algorithm_func(algo_name)
    sizes = np.unique(np.geomspace(min_size, max_size, num=num_steps, dtype=int))

    results = {"sizes": sizes, "times": {}, "fits": {}}

    for dist_name, gen_func in DISTRIBUTIONS.items():
        times = benchmark_c_func(c_func, sizes, gen_func)
        p_opt, _ = curve_fit(timsort_complexity_func, sizes, times)

        results["times"][dist_name] = times
        results["fits"][dist_name] = p_opt

    return results

def run_comparison(
    algo1_name: str,
    algo2_name: str,
    min_size: int = DEFAULT_MIN_SIZE,
    max_size: int = DEFAULT_MAX_SIZE,
    num_steps: int = DEFAULT_NUM_STEPS,
) -> dict:
    """Executes benchmarks to compare two algorithms head-to-head."""
    func1 = get_algorithm_func(algo1_name)
    func2 = get_algorithm_func(algo2_name)
    sizes = np.unique(np.geomspace(min_size, max_size, num=num_steps, dtype=int))

    results = {"sizes": sizes, "algo1_times": {}, "algo2_times": {}}

    for dist_name, gen_func in DISTRIBUTIONS.items():
        results["algo1_times"][dist_name] = benchmark_c_func(func1, sizes, gen_func)
        results["algo2_times"][dist_name] = benchmark_c_func(func2, sizes, gen_func)

    return results
