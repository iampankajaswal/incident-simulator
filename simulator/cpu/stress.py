import multiprocessing
import time


def _consume_cpu(stop_at: float) -> None:
    """
    Busy-loop until the requested end time.

    This intentionally consumes CPU for a bounded period.
    """
    value = 0

    while time.monotonic() < stop_at:
        value = (value + 1) % 1_000_000


def run_cpu_stress(duration: int = 5, workers: int = 1) -> dict:
    """
    Run bounded CPU stress.

    Args:
        duration: Duration in seconds.
        workers: Number of CPU stress processes.

    Returns:
        Result dictionary describing the simulation.
    """
    if duration < 1:
        raise ValueError("duration must be at least 1 second")

    if duration > 60:
        raise ValueError("duration cannot exceed 60 seconds")

    if workers < 1:
        raise ValueError("workers must be at least 1")

    if workers > 4:
        raise ValueError("workers cannot exceed 4")

    stop_at = time.monotonic() + duration

    processes = [
        multiprocessing.Process(
            target=_consume_cpu,
            args=(stop_at,),
        )
        for _ in range(workers)
    ]

    started_at = time.time()

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    completed_at = time.time()

    return {
        "scenario": "high-cpu",
        "status": "completed",
        "duration": duration,
        "workers": workers,
        "elapsed_seconds": round(completed_at - started_at, 2),
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Run bounded CPU stress for incident simulation."
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=5,
        help="Stress duration in seconds.",
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of CPU workers.",
    )

    args = parser.parse_args()

    result = run_cpu_stress(
        duration=args.duration,
        workers=args.workers,
    )

    print("CPU stress completed:")
    print(result)
