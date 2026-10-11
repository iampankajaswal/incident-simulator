
from prometheus_client import CONTENT_TYPE_LATEST, Gauge, generate_latest
from starlette.responses import Response

CPU_STRESS_ACTIVE = Gauge(
    "incident_simulator_cpu_stress_active",
    "Whether the simulated CPU stress scenario is active (1=yes, 0=no).",
)

CPU_STRESS_WORKERS = Gauge(
    "incident_simulator_cpu_stress_workers",
    "Number of workers used by the simulated CPU stress scenario.",
)


def metrics_response() -> Response:
    return Response(
        content=generate_latest(),
        headers={"Content-Type": CONTENT_TYPE_LATEST},
    )

