"""performance.py - Lightweight performance utilities for daily romance email system

Provided utilities:
- @timed: measure and log execution time of functions
- @cache_result(ttl=3600): simple TTL-based in-memory cache for function results
- with_timeout(seconds): context manager to guard API calls against timeouts
- batch_process(iterable, batch_size=10): yield items in fixed-size batches
"""

from __future__ import annotations

import time
import threading
import itertools
import functools
from typing import Any, Callable, Iterable, Iterator, Tuple


def timed(func: Callable) -> Callable:
    """Decorator that times how long a function takes to execute.

    Usage:
      @timed
      def fetch(): ...
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = end - start
        try:
            name = getattr(func, "__name__", str(func))
        except Exception:
            name = str(func)
        print(f"[performance] {name} took {elapsed:.6f}s")
        return result
    return wrapper


def cache_result(ttl: int = 3600) -> Callable[[Callable], Callable]:
    """Decorator to cache function results for a given TTL (in seconds).

    - Supports only hashable arguments for caching. If arguments are not hashable,
      caching is skipped for that call.
    - Thread-safe with internal lock.
    """

    def decorator(func: Callable) -> Callable:
        cache: dict[Tuple[Tuple[Any, ...], Tuple[Tuple[str, Any], ...]], Tuple[Any, float]] = {}
        lock = threading.Lock()

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Build a cache key from args and kwargs. Use a canonical form for kwargs.
            try:
                key_args = tuple(args)
                key_kwargs = tuple(sorted(kwargs.items()))
                key = (key_args, key_kwargs)
            except TypeError:
                # Unhashable arguments; skip caching for this call
                return func(*args, **kwargs)

            now = time.time()
            with lock:
                if key in cache:
                    value, expire = cache[key]
                    if now < expire:
                        return value
                    else:
                        # expired
                        del cache[key]

            # Compute outside the lock to avoid blocking
            result = func(*args, **kwargs)
            with lock:
                cache[key] = (result, now + ttl)
            return result

        # Expose cache for potential inspection in tests (optional)
        wrapper._cache = cache  # type: ignore[attr-defined]
        return wrapper

    return decorator


class _TimeoutContext:
    """Internal timeout context manager using a background timer.

    Notes:
    - This does not forcibly interrupt the code inside the block, but raises a
      TimeoutError when the block exits if execution time exceeded the limit.
    - A timer is used to set a flag when the timeout elapses; on exit, the flag
      is checked and TimeoutError is raised accordingly.
    - Lightweight and suitable for simple API call guards without external deps.
    """

    def __init__(self, seconds: int | float):
        self.seconds = float(seconds)
        self._timed_out = False
        self._timer: threading.Timer | None = None

    def _alarm(self) -> None:
        self._timed_out = True

    def __enter__(self) -> "_TimeoutContext":
        self._timed_out = False
        self._timer = threading.Timer(self.seconds, self._alarm)
        self._timer.daemon = True
        self._timer.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if self._timer is not None:
            self._timer.cancel()
        if self._timed_out:
            raise TimeoutError(f"Operation timed out after {self.seconds} seconds")
        # Do not suppress exceptions in the with-block
        return False


def with_timeout(seconds: int | float) -> _TimeoutContext:
    """Context manager to guard a block of code with a timeout.

    Example:
      with with_timeout(5):
          do_something()
    """
    return _TimeoutContext(seconds)


def batch_process(iterable: Iterable[Any], batch_size: int = 10) -> Iterator[list[Any]]:
    """Yield items from the given iterable in fixed-size batches.

    This helps to process large data sets without loading everything into memory at once.
    """
    if batch_size <= 0:
        raise ValueError("batch_size must be > 0")
    it = iter(iterable)
    while True:
        chunk: list[Any] = list(itertools.islice(it, batch_size))
        if not chunk:
            break
        yield chunk
