"""sort-analyzer: A C/Python hybrid tool to benchmark and analyze sorting algorithms."""

from . import generators
from ._core import run_comparison, run_single_complexity
from .plotting import plot_comparison, plot_complexity

__version__ = "0.2.0"

__all__ = [
    "run_single_complexity",
    "run_comparison",
    "plot_complexity",
    "plot_comparison",
    "generators",
    "__version__",
]
