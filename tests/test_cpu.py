import pytest

from simulator.cpu.stress import run_cpu_stress


def test_cpu_stress_completes():
    result = run_cpu_stress(
        duration=1,
        workers=1,
    )

    assert result["scenario"] == "high-cpu"
    assert result["status"] == "completed"
    assert result["workers"] == 1
    assert result["elapsed_seconds"] >= 1


def test_cpu_duration_cannot_exceed_limit():
    with pytest.raises(ValueError, match="cannot exceed 60"):
        run_cpu_stress(
            duration=61,
            workers=1,
        )


def test_cpu_workers_cannot_exceed_limit():
    with pytest.raises(ValueError, match="cannot exceed 4"):
        run_cpu_stress(
            duration=1,
            workers=5,
        )
