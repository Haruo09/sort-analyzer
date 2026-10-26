import ctypes
import sys
from pathlib import Path


def load_dynamic_lib() -> ctypes.CDLL:
    """Locates and loads the C dynamic library."""
    # Move up 4 levels: _ffi.py -> sort_analyzer -> src -> python -> root
    base_dir = Path(__file__).resolve().parents[3]
    lib_name = "timsort.dll" if sys.platform.startswith("win") else "libtimsort.so"
    lib_path = base_dir / "build" / "lib" / lib_name

    if not lib_path.exists():
        raise FileNotFoundError(
            f"C shared library missing at {lib_path}. Run 'make' first."
        )

    return ctypes.CDLL(str(lib_path))

# Load library singleton
_lib = load_dynamic_lib()


def get_c_function(func_name: str):
    """Retrieves a C function and binds void(int*, int) argtypes/restype."""
    try:
        c_func = getattr(_lib, func_name)
    except AttributeError as err:
        raise AttributeError(f"Function '{func_name}' not found in C library.") from err

    c_func.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
    c_func.restype = None
    return c_func
