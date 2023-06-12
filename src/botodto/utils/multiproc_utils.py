from __future__ import annotations

from multiprocessing import Process, cpu_count
from typing import Callable

from more_itertools import chunked
from tqdm import tqdm

__all__ = ["batch_multiprocess"]


def batch_multiprocess(
    functions: list[Callable],
    n_cores: int = 0,
    show_progress: bool = True,
    desc: str = "",
) -> None:
    """
    Run a list of functions on `n_cores` (default: 0, uses all CPU cores),
    with the option to show a progress bar using tqdm (default: True, shown).
    """
    batches = [*chunked(functions, n_cores or cpu_count())]
    if show_progress:
        batches = tqdm(batches, desc=desc or None)
    for fn_batch in batches:
        process_batch = [Process(target=fn) for fn in fn_batch]
        for proc in process_batch:
            proc.start()
        for proc in process_batch:
            proc.join()
    return
