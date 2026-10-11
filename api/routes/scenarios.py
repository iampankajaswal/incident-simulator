
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from fastapi import APIRouter, HTTPException

from api.metrics import CPU_STRESS_ACTIVE, CPU_STRESS_WORKERS
from api.models import ScenarioRunRequest
from simulator.cpu.stress import run_cpu_stress

router = APIRouter(
    prefix="/scenarios",
    tags=["scenarios"],
)

executor = ThreadPoolExecutor(max_workers=2)
scenario_lock = Lock()
scenario_running = False


def _run_cpu_stress_background(duration: int, workers: int) -> None:
    global scenario_running

    try:
        run_cpu_stress(duration=duration, workers=workers)
    finally:
        CPU_STRESS_ACTIVE.set(0)
        CPU_STRESS_WORKERS.set(0)
        with scenario_lock:
            scenario_running = False


@router.get("")
def list_scenarios() -> dict:
    return {
        "scenarios": [
            {
                "name": "high-cpu",
                "description": "Simulate CPU saturation.",
                "status": "available",
            }
        ]
    }


@router.post("/high-cpu/run")
def run_high_cpu(request: ScenarioRunRequest) -> dict:
    global scenario_running

    with scenario_lock:
        if scenario_running:
            raise HTTPException(
                status_code=409,
                detail="A CPU stress scenario is already running.",
            )

        scenario_running = True
        CPU_STRESS_ACTIVE.set(1)
        CPU_STRESS_WORKERS.set(request.workers)

        try:
            executor.submit(
                _run_cpu_stress_background,
                request.duration,
                request.workers,
            )
        except Exception:
            scenario_running = False
            CPU_STRESS_ACTIVE.set(0)
            CPU_STRESS_WORKERS.set(0)
            raise

    return {
        "scenario": "high-cpu",
        "status": "started",
        "message": (
            f"CPU stress started with {request.workers} worker(s) "
            f"for {request.duration} second(s)."
        ),
    }

