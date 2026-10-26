from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from ._core import (
    ALGORITHM_SYMBOL_MAP,
    DEFAULT_MAX_SIZE,
    DEFAULT_MIN_SIZE,
    DEFAULT_NUM_STEPS,
    run_comparison,
    run_single_complexity,
)
from .plotting import plot_comparison, plot_complexity

app = typer.Typer(
    name="sort-analyzer",
    help="CLI tool to benchmark, analyze, and visualize C sorting algorithms.",
    add_completion=False,
)
console = Console()

VALID_ALGOS = list(ALGORITHM_SYMBOL_MAP.keys())


@app.command("analyze")
def analyze(
    algorithm: str = typer.Argument(
        ...,
        help=f"Algorithm to benchmark. Choices: {', '.join(VALID_ALGOS)}",
    ),
    min_size: int = typer.Option(
        DEFAULT_MIN_SIZE, "--min-size", "-m", help="Minimum array size."
    ),
    max_size: int = typer.Option(
        DEFAULT_MAX_SIZE, "--max-size", "-M", help="Maximum array size."
    ),
    steps: int = typer.Option(
        DEFAULT_NUM_STEPS, "--steps", "-s", help="Number of benchmark evaluation steps."
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Path to save the benchmark plot (e.g. plots/timsort.png)."
    ),
) -> None:
    """Run complexity benchmarks and curve fitting on a single algorithm."""
    algo_clean = algorithm.lower().strip()
    if algo_clean not in ALGORITHM_SYMBOL_MAP:
        console.print(
            f"[bold red]Error:[/bold red] '{algorithm}' is not valid. Choose from: {VALID_ALGOS}"
        )
        raise typer.Exit(code=1)

    console.print(
        Panel.fit(
            f"[bold green]Sort Analyzer[/bold green] - Benchmarking [yellow]{algo_clean}[/yellow]\n"
            f"Array sizes: {min_size:,} -> {max_size:,} across {steps} log steps.",
            border_style="blue",
        )
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(
            description=f"Executing C routines for {algo_clean}...", total=None
        )
        results = run_single_complexity(
            algo_clean, min_size=min_size, max_size=max_size, num_steps=steps
        )

    # Render results table
    table = Table(title=f"Benchmark Results: {algo_clean}")
    table.add_column("Distribution", style="cyan", no_wrap=True)
    table.add_column("Min Size Time (s)", style="magenta")
    table.add_column("Max Size Time (s)", style="green")
    table.add_column("Fitted Parameter (a)", style="yellow")

    for dist_name, times in results["times"].items():
        fit_a = results["fits"][dist_name][0]
        table.add_row(
            dist_name,
            f"{times[0]:.6f}",
            f"{times[-1]:.6f}",
            f"{fit_a:.2e}",
        )

    console.print(table)

    if output:
        plot_complexity(algo_clean, results, output)
        console.print(
            f"[bold green]Plot successfully saved to:[/bold green] {output.resolve()}"
        )


@app.command("compare")
def compare(
    algo1: str = typer.Argument(..., help="First algorithm name."),
    algo2: str = typer.Argument(..., help="Second algorithm name."),
    min_size: int = typer.Option(
        DEFAULT_MIN_SIZE, "--min-size", "-m", help="Minimum array size."
    ),
    max_size: int = typer.Option(
        DEFAULT_MAX_SIZE, "--max-size", "-M", help="Maximum array size."
    ),
    steps: int = typer.Option(
        DEFAULT_NUM_STEPS, "--steps", "-s", help="Number of benchmark evaluation steps."
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Path to save the comparison plot (e.g. plots/compare.png)."
    ),
) -> None:
    """Run head-to-head execution time comparisons between two algorithms."""
    a1, a2 = algo1.lower().strip(), algo2.lower().strip()

    for algo in (a1, a2):
        if algo not in ALGORITHM_SYMBOL_MAP:
            console.print(
                f"[bold red]Error:[/bold red] '{algo}' is not valid. Choose from: {VALID_ALGOS}"
            )
            raise typer.Exit(code=1)

    console.print(
        Panel.fit(
            f"[bold green]Sort Analyzer[/bold green] - Head-to-Head Comparison\n"
            f"[yellow]{a1}[/yellow] vs [yellow]{a2}[/yellow]",
            border_style="magenta",
        )
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(
            description=f"Benchmarking {a1} and {a2} across distributions...",
            total=None,
        )
        results = run_comparison(
            a1, a2, min_size=min_size, max_size=max_size, num_steps=steps
        )

    table = Table(title=f"Comparison: {a1} vs {a2} (Max Size: {max_size:,})")
    table.add_column("Distribution", style="cyan")
    table.add_column(f"{a1} Time (s)", style="yellow")
    table.add_column(f"{a2} Time (s)", style="green")
    table.add_column("Faster Algorithm", style="bold white")

    for dist_name in results["algo1_times"].keys():
        t1 = results["algo1_times"][dist_name][-1]
        t2 = results["algo2_times"][dist_name][-1]
        winner = a1 if t1 < t2 else a2
        diff = abs(t1 - t2) / max(t1, t2) * 100

        table.add_row(
            dist_name,
            f"{t1:.6f}",
            f"{t2:.6f}",
            f"[bold green]{winner}[/bold green] ({diff:.1f}% faster)",
        )

    console.print(table)

    if output:
        plot_comparison(a1, a2, results, output)
        console.print(
            f"[bold green]Plot successfully saved to:[/bold green] {output.resolve()}"
        )


if __name__ == "__main__":
    app()
